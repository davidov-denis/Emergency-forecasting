import os
import pandas as pd
import numpy as np


def strip_data(df):
    return df.replace('^\s+|\s+$', '', regex=True)


def strip_titles(df):
    _ = {}
    for i in df.columns:
        _[i] = i.strip()
    return df.rename(columns=_)


for file in os.listdir('.\data'):
    print(file)
    if ".xlsx" in file:
        df1 = strip_data(pd.read_excel(f"data\{file}"))
        df1 = strip_titles(df1)
        df1.replace("[NULL]", np.nan, inplace=True)
        df1.head()
        df1.to_pickle(f"data/{file.replace(' (1).xlsx', '')}.pkl")
