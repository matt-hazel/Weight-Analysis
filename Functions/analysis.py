# This will be where the analysis section of the data will be.
# I plan to use pandas, plotly, numpy, scipy

from Functions.classes import Measures
from Functions.data_pipe import clean, load, normalize
import pandas as pd
#import plotly.express as px
#import numpy as np
#from scipy import stats


# I need to create a function for viewing the raw data or the clean version.

def raw_read():
    # This function will read the raw data from the csv

    with open (r'data\weight.csv', 'r') as file:
        data = pd.read_csv(file)
        print(data)
    
    
def clean_read():
    # This will be the function that reads out the cleaned data, which will be called during review.
    
    clean(r"data\weight.csv")
    
    with open (r'data\weight_clean.csv', 'r') as file:
            data = pd.read_csv(file)
            print(data)
    
def review():
    # This is where the data science portion of the program will be held, started by calling review().
    ...