# Linear Regression model was not of good fit. Attempting Polynomial Regression

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# load data

df = pd.read_csv(r"data/weight_clean.csv", parse_dates = ['modayr'])
df = df.sort_values("modayr").reset_index(drop=True)

df["day"] = (df["modayr"] - df['modayr'].min()).dt.days


# EWMA model
# "Exponentially Weighted Moving Average" Model


def ewma_trend(df, halflife = 3):
    return df["weight"].ewm(halflife = f"{halflife} days", times = df["modayr"]).mean()

df["ewma"] = ewma_trend(df)
print("THIS IS THE NEW SHIT")
print(df[["modayr", "weight", "ewma"]].tail(10))


def weekly_rate(trend, days, span = 14):
    t, w = days.iloc[-span:], trend.iloc[-span:]
    
    return np.polyfit(t,w,1)[0]*7

print(f"Current trend: {df['ewma'].iloc[-1]:.1f} lbs, rate: {weekly_rate(df['ewma'], df['day']):.2f} lbs/week")


def ewma_forecast(window, horizon = 7, halflife = 3, span = 14):
    trend = ewma_trend(window, halflife)
    rate = weekly_rate(trend, window["day"], span) / 7
    steps = np.arange(1, horizon + 1)
    
    return trend.iloc[-1] + rate * steps

def backtest_ewma(df, halflife, span, horizon = 7, min_train = 21):
    errs, flat_errs, naive_errs = [], [], []
    
    for end in range(min_train, len(df) - horizon + 1):
        window = df.iloc[:end]
        actual = df["weight"].iloc[end:end + horizon].to_numpy()
        
        slope_pred = ewma_forecast(window, horizon, halflife, span)
        flat_pred = ewma_trend(window, halflife).iloc[-1]
        
        errs.append(np.abs(actual - slope_pred).mean())
        flat_errs.append(np.abs(actual - flat_pred).mean())
        naive_errs.append(np.abs(actual - window["weight"].iloc[-1]).mean())
        
    return np.mean(errs), np.mean(flat_errs), np.mean(naive_errs), len(errs)

for hl in (1,2,3,4,5):
    for span in (7, 10, 14):
        slope, flat, naive, runs = backtest_ewma(df, hl, span)
        print(f"half life {hl}d, span {span}: slope {slope:.2f} | flat {flat:.2f} | naive {naive:.2f} | runs {runs}")
        
plt.scatter(df["modayr"], df["weight"], s = 8, c = "r", label = "Weight")
plt.plot(df["modayr"], df["ewma"], c = "b", label = "EWMA trend")
plt.legend()
plt.show()