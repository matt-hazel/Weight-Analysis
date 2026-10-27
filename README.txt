This program is of use for a weight loss/gain journey.

As of 10/27/2026: The Data Science portions are done, along with the trend prediction.
                The model used is a Exponentially Weighted Moving Average (EWMA) hybrid model.
                In combination with EWMA it is a rolling regression model, which aims to correct
                lag in certain postions to decrease the impact of lag in the model's prediction.


The plan is to eventually set up a data analysis portion, where after certain amounts of data has been input,
    the program can make a guess on your progress and analyze the curve of weight gain or loss.
    This will be shown via use of steps, calories consumed, and general activity.

The weight.csv file required for the program will be created upon run of the program and placed inside
data/, and isn't saved to Git, along with the weight_cleaned.csv that is created via the program.
