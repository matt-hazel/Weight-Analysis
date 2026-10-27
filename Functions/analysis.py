# This is where the analysis section of the data is.

from Functions.data_pipe import clean
import pandas as pd


def raw_df():
    return pd.read_csv(r"data\weight.csv")

def clean_df():
    return clean(r"data\weight.csv")

# This returns the recent 7 days of data
def recent_df(source = "raw", days = 7):
    df = clean_df() if source == "cleaned" else raw_df()
    df = df.copy()
    df["modayr"] = pd.to_datetime(df["modayr"], errors="coerce")
    df = df.dropna(subset=["modayr"]).sort_values("modayr").tail(days)
    df["modayr"] = df["modayr"].dt.strftime("%m/%d/%Y")
    
    return df