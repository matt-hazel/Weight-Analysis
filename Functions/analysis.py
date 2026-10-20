# This will be where the analysis section of the data will be.
# I plan to use pandas, plotly, numpy, scipy

from Functions.classes import Measures
from Functions.data_pipe import clean, load, normalize
import pandas as pd
#import plotly.express as px
#import numpy as np
#from scipy import stats


def raw_df():
    return pd.read_csv(r"data\weight.csv")

def clean_df():
    return clean(r"data\weight.csv")

# This returns the recent 7 days of data
def recent_df(days = 7):
    df = raw_df()
    df["modayr"] = pd.to_datetime(df["modayr"], errors = "coerce")
    df = df.dropna(subset = ["modayr"]).sort_values("modayr").tail(days)
    df["modayr"] = df["modayr"].dt.strframe("%m/%d/%Y")
    
    return df



# I need to create a function for viewing the raw data or the clean version.

def raw_read():
    # This function will read the raw data from the csv
    print(raw_df())
    
    
def clean_read():
    # This will be the function that reads out the cleaned data, which will be called during review.
    print(clean_df())
    
def review():
    # This is where the data science portion of the program will be held, started by calling review().
    ...