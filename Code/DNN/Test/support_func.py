import pandas as pd
from numpy import nan, inf
import numpy as np

def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([nan, inf, inf]).any(1)
    return df[indices_to_keep].astype(np.float64)