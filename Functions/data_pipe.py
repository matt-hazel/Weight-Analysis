# This is the file where the cleaning and analysis pipeline is kept.

# Schema for the data:

import csv
import pandas as pd

SCHEMA = {
    "weight" : {"type": "float", "required": True, "min": 50.0, "max": 500.0, "fix": "interpolate"},
    "modayr" : {"type": "date", "required": True},
    "carb" : {"type": "int", "required": True, "min": 0, "max": 1000},
    "fat" : {"type": "int", "required": True, "min": 0, "max": 1000},
    "prot" : {"type": "int", "required": True, "min": 0, "max": 1000},
    "cal" : {"type": "int", "required": True, "min": 0, "max": 10000},
    "steps" : {"type": "int", "required": True, "min": 0, "max": 100000},
    "activ": {"type": "int", "required": True, "min": 0, "max": 2000}
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

def enforce_types(df, schema = SCHEMA):
    # Data types being enforced on the data via the schema
    
    for col, rules in schema.items():
        if col not in df:
            raise KeyError(f"Missing column {col}")
        t = rules["type"]
        if t == "date":
            df[col] = pd.to_datetime(df[col], errors="coerce")
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce") # Bad values turn to NaN
            
    return df
    
def enforce_ranges(df, schema = SCHEMA):
    # Enforcing the ranges of the data via the schema
    
    for col, rule in schema.items():
        if "min" in rule:
            df.loc[df[col] < rule["min"], col] = pd.NA
        if "max" in rule:
            df.loc[df[col] > rule["max"], col] = pd.NA
    return df

def apply_fixes(df, schema = SCHEMA):
    # Applies fixes to the data based on schema rules.
    
    for col, rule in schema.items():
        if "fix" in rule:
            if rule["fix"] == "interpolate":
                df[col] = df[col].interpolate()
    return df

def drop_missing(df, schema = SCHEMA):
    # Drops rows with missing vals
    
    required = [c for c, r in schema.items() if r.get("required")]
    return df.dropna(subset = required)

def finalize_types(df, schema = SCHEMA):
    # finalizes the data types of the data
    
    for col, rule in schema.items():
        if rule["type"] == "int":
            df[col] = df[col].astype(int)
        elif rule["type"] == "float":
            df[col] = df[col].astype(float)
    
    return df

def clean(path, schema = SCHEMA):
    # This is the function that will clean the data
    df = load(path)
    df = normalize(df)
    df = enforce_types(df, schema)
    df = enforce_ranges(df, schema)
    df = apply_fixes(df, schema)
    df = drop_missing(df, schema)
    df = finalize_types(df, schema)
    
    df = df.drop_duplicates(subset = "modayr").reset_index(drop = True)
    df.to_csv(r"data\weight_clean.csv", index=False)
    
    return df
    # Perform cleaning operations on df
