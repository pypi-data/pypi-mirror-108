import pandas as pd
import numpy as np
from typing import List, Dict
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from math import sqrt


def create_mini_table(original_df: pd.DataFrame, cols_for_reduced_df: List[str]) -> pd.DataFrame:
    """
    Extract only relevant columns from dataframe
    :param original_df: pd.DataFrame initially preprocessed dataframe
    :param cols_for_reduced_df: list of column names
    :return: df: pd.DataFrame with relevant columns
    """
    df = original_df[cols_for_reduced_df]
    df = df.drop_duplicates()

    return df


def remove_out_of_panel_genes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows containing variants and genes which were removed from panel
    :param: df: src pd.DataFrame
    :return: new_df: pd.DataFrame after cleaning
    """
    new_df = df[(df['name'] != 'BCHE') & (df['name'] != 'ABCA4') & (df['display_label'] != 'g.27134T>G')]

    return new_df


def remove_by_sheba_instructions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows containing specific sample_number formats and unknown cases
    :param: df:pd.DataFrame
    :return: pd.DataFrame after cleaning
    """
    df = df[~df.sample_number.str.contains('D|-', regex=True)]
    df = df[df['transfer_to'] != 'UNKNOWN']

    return df


def convert_lists_to_strings(df: pd.DataFrame, col_name: str) -> pd.DataFrame:
    """
    Replace lists with joined strings
    :param: df:pd.DataFrame cleaned dataframe
    :param: col_name:str The name of column containing lists
    :return:df:pd.DataFrame with joined strings
    """
    df[col_name] = df[col_name].apply(lambda x: [i for i in x if str(i) != "None"])
    df[col_name] = df[col_name].apply(', '.join)

    return df


def organize_data(df: pd.DataFrame, col_to_sort: str, colname1_to_str: str, colname2_to_str: str) -> pd.DataFrame:
    """
    Sort Dataframe, remove None, convert lists to strings and remove duplicates
    :param df:pd.DataFrame The cleaned DataFrame
    :param col_to_sort:str name of column we want to sort by
    :param colname1_to_str:str name of column we want to convert its lists to str
    :param colname2_to_str:str name of column we want to convert its lists to str
    :return:df_temp:pd.DataFrame after initial preprocess
    """
    df = df.sort_values(by=[col_to_sort])
    df = df.replace({None: ""})
    df_temp = df.copy()

    convert_lists_to_strings(df_temp, colname1_to_str)
    convert_lists_to_strings(df_temp, colname2_to_str)
    df_temp = df_temp.drop_duplicates()

    return df_temp


def split_pname(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split the pname string
    :param df:pd.DataFrame The cleaned DataFrame
    :return: A DataFrame with split pname
    """
    df[['p', 'rest_a']] = df.primary_pname.str.split('.', 1, expand=True)
    df[['amino_a', 'pos_amino', 'amino_b']] = df.rest_a.str.extract('([A-Za-z]+)(\d+\.?\d*)([A-Za-z]+)', expand=True)

    df.drop(['rest_a'], axis=1, inplace=True)

    return df


def remove_duplications_dmd(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove duplications of DMD gene per each id
    :param df:pd.DataFrame The cleaned DataFrame
    :return: new_df: pd.DataFrame with first variant of DMD per each id
    """
    df = df.copy()
    dmd_df = df[df['name'] == 'DMD']
    df = df[df['name'] != 'DMD']
    dmd_df.drop_duplicates(subset=['id', 'name', 'comment'], keep='first', inplace=True)
    new_df = pd.concat([df, dmd_df])

    return new_df


def preprocess_raw_data(df: pd.DataFrame, cols_for_reduced_df: List['str']) -> pd.DataFrame:
    """
    Manage initial preprocess of raw data
    :param df:pd.DataFrame The src DataFrame
    :param cols_for_reduced_df: List['str'] names of columns
    :return: preprocessed_df: pd.DataFrame processed
    """
    preprocessed_df = organize_data(df, 'id', 'transfer_to', 'comment')
    preprocessed_df = create_mini_table(preprocessed_df, cols_for_reduced_df)
    preprocessed_df = remove_out_of_panel_genes(preprocessed_df)
    preprocessed_df = remove_by_sheba_instructions(preprocessed_df)
    preprocessed_df = split_pname(preprocessed_df)
    preprocessed_df = remove_duplications_dmd(preprocessed_df)

    return preprocessed_df


def extract_overrides(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract overrides from the preprocessed dataframe.
    :param df:pd.DataFrame preprocessed DataFrame from which we extract the overrides.
    :return: A DataFrame containing only overrides.
    """
    overrides_df = df[(df['transfer_from'] != '') & (df['transfer_to'] != '')]

    return overrides_df


def extract_non_overrides(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract non overrides from preprocessed dataframe.
    :param df:pd.DataFrame preprocessed DataFrame from which we extract the non overrides.
    :return: df:pd.DataFrame A DataFrame containing only non overrides.
    """
    non_overrides_df = df[(df['transfer_from'] == '') & (df['transfer_to'] == '') & (df['result_id'] != '')]
    non_overrides_df = non_overrides_df.copy()
    non_overrides_df.dropna(subset = ['result_id'], inplace=True)

    return non_overrides_df


def lower_case_col(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Turn all str in dataframe column to lowercase
    :param df:pd.DataFrame
    :param col: str. name of column
    :return: df:pd.DataFrame with lowercase strings column
    """
    df = df.copy()
    df[col] = df[col].str.lower()

    return df


def replace_string(df: pd.DataFrame, from_str: str, to_str: str) -> pd.DataFrame:
    """
    Replaces one string in another
    :param df: pd.DataFrame
    :param from_str: str. string to replace
    :param to_str: str. replace to string
    :return: df:pd.DataFrame after replacement
    """
    df = df.copy()
    df['comment'] = df['comment'].str.replace(from_str, to_str)

    return df


def replace_strings_in_comment(df: pd.DataFrame) -> pd.DataFrame:
    """
    Correct spelling mistakes in the comment column
    :param df:pd.DataFrame
    :return: df:pd.DataFrame with corrected spelling mistakes in comments column
    """
    df = replace_string(df, 'nc', 'nocall')
    df = replace_string(df, 'no call', 'nocall')
    df = replace_string(df, 'probe to probe', 'probe_to_probe')
    df = replace_string(df, 'prob to prob', 'probe_to_probe')
    df = replace_string(df, 'probe to prob', 'probe_to_probe')
    df = replace_string(df, 'prob to probe', 'probe_to_probe')
    df = replace_string(df, 'prob to probe', 'probe_to_probe')

    return df


def remove_special_chars(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove special characters from the comment column
    :param df:pd.DataFrame
    :return: df:pd.DataFrame with chained comments in comments column
    """
    df['chain_comment'] = df['comment'].str.replace('[^\w\s]', '', regex=True)
    df['chain_comment'] = df['chain_comment'].str.replace('\W', '', regex=True)

    return df


def remove_missing_comments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove overrides cases without comments (considered a bug in software)
    :param df:pd.DataFrame containing only overrides.
    :return: new_df:pd.DataFrame the overrides dataframe with comments only.
    """
    new_df = df[df['comment'] != '']

    return new_df


def remove_special_cases(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove cases we cannot predict as overrides
    :param df:pd.DataFrame containing only overrides.
    :return: df:pd.DataFrame with comments that we cannot predict by model
    """
    df = df[df['comment'].str.count(r'[0-9][0-9]\s*.*nocall') == 0]
    df = df[df['comment'].str.count(r'nocall\s*.*[0-9][0-9]') == 0]
    df = df[df['comment'].str.count('תקין בסאנגר') == 0]
    df = df[df['comment'].str.count('תקין ב-סאנגר') == 0]
    df = df[df['comment'].str.count('תקין בסנגר') == 0]
    df = df[df['comment'].str.count('תקין סאנגר') == 0]
    df = df[df['comment'].str.count('סרנגר') == 0]
    df = df[df['comment'].str.count('סאנגר') == 0]
    df = df[df['comment'].str.count('סנגר') == 0]
    df = df[df['comment'].str.count('תקין בריצוף') == 0]
    df = df[df['comment'].str.count('תקין בננו') == 0]
    df = df[df['comment'].str.count('mlpa') == 0]
    df = df[df['comment'].str.count('malpa') == 0]
    df = df[df['comment'].str.count('נשא בסאנגר') == 0]
    df = df[df['comment'].str.count('קווקזי') == 0]
    df = df[df['comment'].str.count('קווקזי') == 0]
    df = df[df['comment'].str.count('sanger') == 0]

    return df


def show_overrides_history(df: pd.DataFrame) -> pd.DataFrame:
    """
    Split overrides cases to columns representing history of overrides
    :param df:pd.DataFrame containing only overrides.
    :return: df:pd.DataFrame with overrides history.
    """
    df = pd.concat([df, df.transfer_to.str.split(', ', expand=True).add_prefix('trans_to_No_')], axis=1)
    df = pd.concat([df, df.comment.str.split(', ', expand=True).add_prefix('comment_No_')], axis=1)

    return df


def clean_overrides_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean overrides dataframe by all steps functions
    :param df:pd.DataFrame containing only overrides
    :return: new_df:pd.DataFrame cleaned
    """
    new_df = lower_case_col(df, 'comment')
    new_df = replace_strings_in_comment(new_df)
    new_df = remove_special_chars(new_df)
    new_df = remove_missing_comments(new_df)
    new_df = remove_special_cases(new_df)
    # new_df = show_overrides_history(new_df)

    return new_df


def create_tot_df(overrides_df: pd.DataFrame, non_overrides_df: pd.DataFrame) -> pd.DataFrame:
    """
    create full table containing overrides and non_overrides labeled
    :param: overrides_df: pd.DataFrame cleaned overrides_df
    :param: non_overrides_df: pd.DataFrame cleaned non_overrides_df
    :return: tot_df: pd.DataFrame containing labels created for clusters
    """
    random_non_overrides = non_overrides_df.sample(n=400)
    frames = [random_non_overrides, overrides_df]
    tot_df = pd.concat(frames)

    return tot_df


def add_label_col(non_overrides_df: pd.DataFrame, overrides_df: pd.DataFrame) -> pd.DataFrame:
    """
    add column containing constant value for overrides -label 1, and for non overrides- label
    :param non_overrides_df:pd.DataFrame containing only non overrides
    :param overrides_df:pd.DataFrame containing only overrides
    :return: all_cases_df:pd.DataFrame concatenated dataframe of labeled overrides and non overrides
    """
    overrides_labeled = overrides_df.copy()
    non_overrides_labeled = non_overrides_df.copy()

    overrides_labeled['label'] = 1
    non_overrides_labeled['label'] = 0

    all_cases_df = create_tot_df(overrides_labeled, non_overrides_labeled)

    return all_cases_df


def grouping_by_comments(df: pd.DataFrame) -> pd.DataFrame:
    """
    group dataframe by comments and arrange by frequency of appearances
    :param df:pd.DataFrame containing only overrides
    :return: grouped_df:pd.DataFrame grouped by comments
    """
    grouped_df = df.groupby(['chain_comment']).agg({'result_id': 'count'}).reset_index()
    grouped_df.sort_values(by=['result_id'], ascending=False, inplace=True)

    return grouped_df


def get_common(df: pd.DataFrame, col: str, threshold: int) -> pd.DataFrame:
    """
    Get a dataframe containing values above certain threshold
    :param df:pd.DataFrame containing only overrides
    :param col:str name of column containing values to be filtered
    :param threshold:int threshold for filtering values
    :return: common_df:pd.DataFrame filtered by threshold
    """
    common_df = df[df[col] >= threshold]

    return common_df


def extract_common_comments(overrides_df: pd.DataFrame, common_comments_df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract only the rows with common comments from the cleaned overrides dataframe
    :param overrides_df:pd.DataFrame containing only overrides
    :param common_comments_df:pd.DataFrame of grouped common comments
    :return df_new:pd.DataFrame of common comments overrides
    """
    df_new = overrides_df[overrides_df.chain_comment.isin(common_comments_df.chain_comment)]

    return df_new


def process_common_comments(overrides_df: pd.DataFrame) -> pd.DataFrame:
    """
    group by comments and extract most common overrides
    :param overrides_df:pd.DataFrame containing only overrides
    :return: full_common_comments:pd.DataFrame containing only overrides with common comments
    """
    grouped_comments = grouping_by_comments(overrides_df)
    common_comments_df = get_common(grouped_comments, 'result_id', 4)
    full_common_comments = extract_common_comments(overrides_df, common_comments_df)

    return full_common_comments


def preprocess_overrides(df: pd.DataFrame) -> pd.DataFrame:
    """
    preprocess overrides df by filtering and editing functions
    :param overrides_df:pd.DataFrame containing only overrides
    :return: full_common_comments:pd.DataFrame containing only overrides with common comments
    """
    overrides_df = extract_overrides(df)
    overrides_df = replace_strings_in_comment(overrides_df)
    # important- for extract df for binary classification we reduce the cases of overrides by clean_overrides_data
    overrides_df = clean_overrides_data(overrides_df)
    overrides_df = show_overrides_history(overrides_df)

    return overrides_df


def create_features_df_tl(df: pd.DataFrame) -> pd.DataFrame:
    """
    extract features for model from the overrides dataframe with most common comments
    :param df:pd.DataFrame containing only overrides with most common comments
    :return: features_df:pd.DataFrame containing features for model
    """
    features_df = df[['name', 'gender', 'clinical_significance', 'ref', 'alt', 'hg38_start', 'Paternal Gradma',
                      'amino_a', 'pos_amino', 'amino_b', 'Paternal Gradpa', 'Maternal Gradma', 'Maternal Gradpa',
                      'chromosome', 'label']]
    features_df = features_df.sample(frac=1)

    return features_df


def create_features_df(df: pd.DataFrame) -> pd.DataFrame:
    """
    extract features for model from the overrides dataframe with most common comments
    :param df:pd.DataFrame containing only overrides with most common comments
    :return: features_df:pd.DataFrame containing features for model
    """
    features_df = df[['name', 'gender', 'clinical_significance', 'ref', 'alt', 'hg38_start', 'Paternal Gradma', 'amino_a',
                      'pos_amino', 'amino_b', 'Paternal Gradpa', 'Maternal Gradma', 'Maternal Gradpa', 'chromosome']]

    return features_df


def fill_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    fill missing data for variants who don't have change in protein (without pname)
    :param df:pd.DataFrame features
    :return: df:pd.DataFrame features with no missing data
    """
    df = df.copy()
    df['amino_a'] = np.where(df['amino_a'].notna(), df['amino_a'], 'No aa')
    df['amino_b'] = np.where(df['amino_b'].notna(), df['amino_b'], 'No aa')
    df['pos_amino'] = np.where(df['pos_amino'].notna(), df['pos_amino'], 0)

    return df


def apply_sc_to_cols(df: pd.DataFrame, cols_list: List[str]) -> pd.DataFrame:
    """
    Apply standard scaler to numerical features.
    :param: df:pd.DataFrame The features DataFrame.
    :param: cols_list: List(str) of column names.
    :return: pd.DataFrame scaled dataframe
    """
    sc = StandardScaler()
    df = df.copy()
    df[cols_list] = sc.fit_transform(df[cols_list])

    return df


def handle_categorical_features(df: pd.DataFrame, categorical_cols: List[str]) -> pd.DataFrame:
    """
    Apply one hot encoding on categorical features.
    :param df:pd.DataFrame The features dataframe.
    :param categorical_cols:List[str] name of columns containing categorical features
    :return: pd.DataFrame one hot encoded dataframe
    """
    df_one_hot = pd.get_dummies(df, columns=categorical_cols)

    return df_one_hot


def process_features(df: pd.DataFrame, categorical_cols) -> pd.DataFrame:
    """
    manage the features processing
    :param: df:pd.DataFrame The features dataframe
    :return: pd.DataFrame processed features
    """
    df = fill_missing_data(df)
    scaled_df = apply_sc_to_cols(df, ['hg38_start', 'pos_amino'])
    processed_df = handle_categorical_features(scaled_df, categorical_cols)

    return processed_df


def calculate_wcss(df, kmax) -> List[float]:
    """
    calculate Within Cluster Sum of Squares for kmeans clusters
    :param: df:pd.DataFrame The features dataframe
    :param: kmax:int max number of groups for clustering
    :return: wcss: List[float] list of calculated wcss per each cluster
    """
    wcss = []
    K = range(2, kmax+1)
    for k in K:
        kmeans = KMeans(n_clusters=k, init='k-means++', random_state=3425)
        kmeans.fit(df)
        wcss.append(kmeans.inertia_)

    return wcss


def optimal_number_of_clusters(wcss: List[float], kmax: int) -> int:
    """
    find the optimal number of clusters by the formula of distance between a point and a line
    :param: wcss: List[float] list of calculated wcss per each cluster
    :param: kmax: max number of groups for clustering
    :return: optimal_n_clusters: int
    """
    x1, y1 = 2, wcss[0]
    x2, y2 = kmax+1, wcss[len(wcss) - 1]

    distances = []
    for i in range(len(wcss)):
        x0 = i + 1
        y0 = wcss[i]
        numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
        denominator = sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
        distances.append(numerator / denominator)

    optimal_n_clusters = distances.index(max(distances)) + 2

    return optimal_n_clusters


def wcss_calcs(df: pd.DataFrame) -> int:
    """
    manage wcss calcs
    :param: df:pd.DataFrame features dataframe
    :return: optimal_n_clusters: int
    """
    wcss = calculate_wcss(df, 40)
    optimal_n_clusters = optimal_number_of_clusters(wcss, 40)

    return optimal_n_clusters


def apply_kmeans(df: pd.DataFrame, optimal_n_clusters: int) -> int:
    """
    apply kmeans model for clustering
    :param: df:pd.DataFrame features dataframe
    :param: optimal_n_clusters: int
    :return: label:int ndarray: containing labels created for clusters
    """
    kmeans = KMeans(n_clusters=optimal_n_clusters)
    label = kmeans.fit_predict(df)
    # cluster_centers = np.array(kmeans.cluster_centers_)

    df['label'] = label
    centroids = kmeans.cluster_centers_
    print(centroids)

    return label








