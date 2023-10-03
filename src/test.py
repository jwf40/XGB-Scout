import pandas as pd
from dataloader import YearlyDataLoader

YEAR_SET = {"2019-20", "2020-21", "2021-22", "2022-23", "2023-24"}


def test_yearlydloader():
    for year in YEAR_SET:
        ydl = YearlyDataLoader(year=year, gws=None)
        assert isinstance(ydl, YearlyDataLoader)


def test_teamcodes():
    for year in YEAR_SET:
        ydl = YearlyDataLoader(year=year, gws=None)
        assert ydl.team_code2name[ydl.team_name2code["Arsenal"]] == "Arsenal"
        assert ydl.team_code2name[1] == "Arsenal"
        ydl = YearlyDataLoader(year=year, gws=None)
        assert ydl.team_code2name[ydl.team_name2code["Chelsea"]] == "Chelsea"


def test_teamdifficulty():
    for year in YEAR_SET:
        ydl = YearlyDataLoader(year=year, gws=None)
        assert ydl.team_difficulty[ydl.team_name2code["Man City"]] == 5
        assert ydl.team_difficulty[ydl.team_name2code["Arsenal"]] == 4


# def test_gwdict():
#     ydl = YearlyDataLoader(year='2020-21', gws=None)


# def test_csvtodf():
#     ydl = YearlyDataLoader(year='2020-21', gws=None)
