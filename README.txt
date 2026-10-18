This program is of use for a weight loss/gain journey.

The packages used are:
    time, csv, path, pandas, plotly, numpy, scipy, os, subprocess, 

As of 10/16/2026: There is full terminal menu functionality, CSV writing and raw reading, automatic package detection
    and if needed also install, along with a set architecture. Current plan is to get the data science portion set up.
    As of now, getting the cleaning functionality set up is the current objective.

10/17/2026 11:41PM: Got full auto cleaning of data set up via SCHEMA held in data_pipe.py

The plan is to eventually set up a data analysis portion, where after certain amounts of data has been input,
    the program can make a guess on your progress and analyze the curve of weight gain or loss.
    This will be shown via use of steps, calories consumed, and general activity.

The weight.csv file required for the program will be created upon run of the program and placed inside
data/, and isn't saved to Git.
