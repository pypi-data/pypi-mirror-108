import pandas as pd
from lab_overrides.featureextraction import featureextraction as fe


COLS_FOR_REDUCED_DF = ['id', 'result_id', 'sample_number', 'panel_type', 'gender', 'offering_id', 'name',
                         'display_label', 'primary_full_name', 'chromosome', 'result_status', 'clinical_significance',
                         'transfer_from', 'transfer_to', 'comment', 'Paternal Gradma', 'Paternal Gradpa',
                         'Maternal Gradma', 'Maternal Gradpa', 'sc_created', 'lab_report_date', 'gc_report_date', 'ref',
                         'alt', 'primary_pname', 'hg38_start']

CATEGORICAL_FEATURES = ['name', 'gender', 'clinical_significance', 'ref', 'alt', 'Paternal Gradma', 'Paternal Gradpa',
                         'Maternal Gradma', 'Maternal Gradpa', 'amino_a', 'amino_b', 'chromosome']


def extract_features_for_binary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract features df for binary classification - label 0 for non-overrides and label 1 for overrides
    :param df:pd.DataFrame The src DataFrame
    :return:binary_features: pd.DataFrame
    """
    non_overrides_df = fe.extract_non_overrides(df)
    overrides_df = fe.preprocess_overrides(df)
    binary_df = fe.add_label_col(non_overrides_df, overrides_df)
    binary_df_tl = fe.create_features_df_tl(binary_df)
    binary_df_tl.to_pickle('/Users/tovahallas/projects/ml_missions/raw_data/binary_df_tl.pkl')
    binary_features = fe.create_features_df(binary_df)
    binary_features = fe.process_features(binary_features, CATEGORICAL_FEATURES)
    binary_features['label'] = binary_df['label']


    return binary_features


def extract_features_for_overrides(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract features df for binary overrides comments
    :param df:pd.DataFrame The src DataFrame
    :return:overrides_features: pd.DataFrame
    """
    overrides_df = fe.preprocess_overrides(df)
    overrides_df = fe.process_common_comments(overrides_df)
    overrides_features = fe.create_features_df(overrides_df)
    overrides_features_tl = overrides_features.copy()
    overrides_features = fe.process_features(overrides_features, CATEGORICAL_FEATURES)
    optimal_n_clusters = fe.wcss_calcs(overrides_features)
    label = fe.apply_kmeans(overrides_features, optimal_n_clusters)

    overrides_features['label'] = label
    overrides_features['chain_comment'] = overrides_df['chain_comment']

    overrides_features_tl['label'] = label
    overrides_features_tl['chain_comment'] = overrides_df['chain_comment']
    overrides_features_tl.to_pickle('/Users/tovahallas/projects/ml_missions/raw_data/overrides_features_tl.pkl')

    return overrides_features


def display_overrides_df():
    """
    display the preprocessed features of overrides and the comments labeled
    """
    dataset = pd.read_pickle('/Users/tovahallas/projects/ml_missions/raw_data/raw_df.pkl')
    preprocessed_data = fe.preprocess_raw_data(dataset, COLS_FOR_REDUCED_DF)
    overrides_features = extract_features_for_overrides(preprocessed_data)

    print(overrides_features)


def display_binary_classification_df():
    """
    display the preprocessed features of binary classification
    """
    dataset = pd.read_pickle('/Users/tovahallas/projects/ml_missions/raw_data/raw_df.pkl')
    preprocessed_data = fe.preprocess_raw_data(dataset, COLS_FOR_REDUCED_DF)
    binary_features = extract_features_for_binary(preprocessed_data)
    binary_features.to_pickle('/Users/tovahallas/projects/ml_missions/raw_data/binary_features.pkl')

    print(binary_features)


if __name__ == '__main__':
    # display_overrides_df()
    # display_overrides_df()
    display_binary_classification_df()

    print('done')

