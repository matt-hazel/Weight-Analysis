# This is where the analysis section of the data is.

from Functions.data_pipe import clean
from pathlib import Path
import pandas as pd


DATA_FILES = [Path("data/weight.csv"), Path("data/weight_clean.csv")]
COLUMNS = ["weight", "modayr", "carb", "fat", "prot", "cal", "steps", "activ"]


def clear_data():
    for f in DATA_FILES:
        f.unlink(missing_ok = True)

def raw_df():
    path = Path("data/weight.csv")
    
    if not path.exists():
        return pd.DataFrame(columns = COLUMNS)
    
    return pd.read_csv(path)

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

def has_data():
    return len(raw_df()) > 0

