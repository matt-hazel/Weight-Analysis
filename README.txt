This program is of use for a weight loss/gain journey.

The packages used are:
    time, csv, path, pandas, plotly, numpy, scipy, os, subprocess, statsmodels

As of 10/20/2026: There is full terminal menu functionality, CSV writing and raw reading, automatic package detection
    and if needed also install, along with a set architecture. The data review has been set up in a flask dashboard,
    and I have plans to move the terminal menu into said flask dashboard as well, phasing out the terminal menu.
    As of now, it shows off a number of plots related to the user's weight journey and allows for the user to 
    view the trends of their data.

10/20/2026: As of 12:40PM, basic web dashboard has been created, plots on button activated display.
                I plan to do further work on them, matrix looks iffy, along with one other. 
                Once this is completed, I will move on to phasing out the terminal based interface.

The plan is to eventually set up a data analysis portion, where after certain amounts of data has been input,
    the program can make a guess on your progress and analyze the curve of weight gain or loss.
    This will be shown via use of steps, calories consumed, and general activity.

The weight.csv file required for the program will be created upon run of the program and placed inside
data/, and isn't saved to Git, along with the weight_cleaned.csv that is created via the program.
