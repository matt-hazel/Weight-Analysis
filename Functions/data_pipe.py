# This is the file where the cleaning and analysis pipeline is kept.

# Schema for the data:

import csv
import pandas as pd

SCHEMA = {
    "weight" : {"type": "float", "required": True, "min": 0.0, "max": 500.0, "fix": "interpolate"},
    "modayr" : {"type": "date", "required": True},
    "carb" : {"type": "int", "required": True, "min": 0},
    "fat" : {"type": "int", "required": True, "min": 0},
    "prot" : {"type": "int", "required": True, "min": 0},
    "cal" : {"type": "int", "required": True, "min": 0},
    "steps" : {"type": "int", "required": True, "min": 0},
    "activ": {"type": "int", "required": True, "min": 0}
}

def load(path, schema = SCHEMA):
    # Loading the data from weight.csv
    return pd.read_csv(path)


def normalize(df):
    # This is where the data will be normalized for analysis.
    
    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    
    for col in df.select_dtypes("object"):
        df[col] = df[col].str.strip()
        
    df = df.replace("", pd.NA)
    
    df["modayr"] = pd.to_datetime(df["modayr"], errors="coerce")
    
    df_sorted = df.sort_values(by="modayr", ascending=True)
        
    df_sorted.to_csv(r"data\\weight_clean.csv", index=False)
    
    return df_sorted

def clean(path, schema = SCHEMA):
    # This is the function that will clean the data
    df = load(path)
    normalize(df)
    # Perform cleaning operations on df
