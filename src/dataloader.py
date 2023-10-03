from typing import Tuple, List, Union, Optional
import numpy as np
import pandas as pd
import xgboost as xgb
import os

"""
Assumed Data File Format:
    root_data_folder/year_folders/                                                               
                                - teams.csv
                                - gws/ [folder]
                                    - gwX.csv [files]
                                - players/ [folder]
"""


class YearlyDataLoader:
    """
    Class for loading and interfacing with raw data csv files from a single year and converting them into useable training data
    """

    def __init__(
        self,
        year: str,
        gws: Union[None, List[str]],
        data_root: Optional[str] = "src/data",
        teams_csv_path: Optional[str] = "src/master_team_list.csv",
        features: Optional[List[str]] = None,
    ) -> None:
        """
        ||year: str => year to get data from.
        ||gws: Union[None, List[str]] => gameweeks to get data from. Set to None to get all
        ||data_root: Optional[str] => root folder for csv data
        ||teams_csv: Optional[str] => path to teams data csv file
        ||features: Optional[List[str]] => list of features to take from gameweek csvs. Leave blank to take all.
        """
        self.root = data_root
        self.teams_csv_path = teams_csv_path
        self.year = year
        self.features = features

        self.team_code2name, self.team_name2code = self.get_codes_names()

        self.gw_root = f"{self.root}/{self.year}/gws/"
        self.gws = (
            gws if gws else [f"gw{idx}" for idx in range(1, self.get_num_gws() + 1)]
        )

        self.team_difficulty = self.get_team_difficulty()

        self.df_dict = {f"{gw}": self.csv_to_df(gw) for gw in self.gws}

    def get_codes_names(self) -> Tuple[dict, dict]:
        """
        Gets the mapping from team codes to names, and vice versa
        """
        team_df = pd.read_csv(self.teams_csv_path, encoding="latin-1")
        team_df = team_df.loc[team_df["season"] == self.year]
        code2name = dict()
        name2code = dict()
        for idx, row in team_df.iterrows():
            code2name[row["team"]] = row["team_name"]
            name2code[row["team_name"]] = row["team"]
        return code2name, name2code

    def get_num_gws(self) -> int:
        """
        Get the number of gameweeks based on file names
        """
        # get list of all gw csv files
        gw_str = sorted(
            filter(lambda x: x[:2] == "gw", list(os.listdir(self.gw_root)))
        )[-1]
        gw_str = gw_str.split(".")[0][2:]
        return int(gw_str)

    def csv_to_df(self, gw: str, encoding="latin-1", **kwargs) -> pd.DataFrame:
        """
        Reads in a csv file to Pandas DataFrame.
        ||gw: str => gw to read csv from
        """
        path = self.gw_root + f"{gw}.csv"
        df = pd.read_csv(path, encoding=encoding, **kwargs)
        # Fixture difficulty is stored in different csv, read it in in needed
        if not self.features or (self.features and "fdr" in self.features):
            fdr = [self.team_difficulty[code] for code in df["opponent_team"]]
            df["fdr"] = fdr
        if self.features:
            df = df[self.features]
        return df

    def get_team_difficulty(self) -> dict:
        """
        Read from teams.csv to get team codes and their strength data
        """
        difficulty_root = f"{self.root}/{self.year}/teams.csv"
        teams_df = pd.read_csv(difficulty_root)
        name_to_code = [self.team_name2code[name] for name in teams_df["name"]]
        fdr = {code: fdr for code, fdr in zip(name_to_code, teams_df["strength"])}
        return fdr
