import numpy as np
import pandas as pd
import xgboost as xgb

class DataInterface():
    def __init__(self, years: list, gws: list)->None:
        pass

    def csv_to_df(self, path: str, **kwargs)->pd.DataFrame:
        """
        Reads in a csv file to Pandas DataFrame.
        Removes need to import Pandas elsewhere.
        || path: string | path to csv file
        """
        return pd.read_csv(path, **kwargs)

    def get_fixture_difficulty(self):
        """
        Read from fixtures.csv within each year folder
        """
        pass