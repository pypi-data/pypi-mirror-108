from src.lab_overrides.dal import connect_db as cdb
import pandas as pd


def connect_to_db():
    """
    connect to postgres db
    :return: raw_df:pd.DataFrame: raw data table
    """
    # connect to db and convert to pandas dataframe
    conn_param = cdb.DBConnection()
    conn_param = conn_param.connect()
    raw_df = cdb.SQLtodf(conn_param)
    raw_df = raw_df.sql_to_df()

    return raw_df


def create():
    """
    create pandas dataframe from postgres database
    """
    raw_df = connect_to_db()
    raw_df.to_pickle('/Users/tovahallas/projects/ml_missions/raw_data/raw_df.pkl')


if __name__ == '__main__':
    create()


