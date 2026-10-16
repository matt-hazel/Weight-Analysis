# This will be where the analysis section of the data will be.
# I plan to use pandas, plotly, numpy, scipy

#from classes import Measures
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