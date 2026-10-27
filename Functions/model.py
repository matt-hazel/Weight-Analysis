# Linear Regression model was not of good fit. Attempting Polynomial Regression

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression
from scipy.optimize import curve_fit

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#for the multi testing
import glob
from itertools import product


# load data

df = pd.read_csv(r"data/training/user_01.csv", parse_dates = ['modayr'])
df = df.sort_values("modayr").reset_index(drop=True)

df["day"] = (df["modayr"] - df['modayr'].min()).dt.days


# EWMA model
# "Exponentially Weighted Moving Average" Model


def ewma_trend(df, halflife = 1.5):
    return df["weight"].ewm(halflife = f"{halflife} days", times = df["modayr"]).mean()

df["ewma"] = ewma_trend(df)


def weekly_rate(trend, days, span = 14):
    t, w = days.iloc[-span:], trend.iloc[-span:]
    
    return np.polyfit(t,w,1)[0]*7

print(f"Current trend: {df['ewma'].iloc[-1]:.1f} lbs, rate: {weekly_rate(df['ewma'], df['day']):.2f} lbs/week")


def ewma_forecast(window, horizon = 7, halflife = 1.5, span = 14):
    trend = ewma_trend(window, halflife)
    rate = weekly_rate(trend, window["day"], span) / 7
    steps = np.arange(1, horizon + 1)
    
    return trend.iloc[-1] + rate * steps

def ewma_forecast_lag(window, horizon = 7, halflife = 1.5, span = 14):
    trend = ewma_trend(window, halflife)
    rate = weekly_rate(trend, window["day"], span) / 7
    lag = halflife / np.log(2)
    steps = np.arange(1, horizon + 1)
    
    return trend.iloc[-1] + rate * (steps + lag)


def backtest_ewma(df, halflife, span, horizon = 7, min_train = 21, step = 1):
    scores = {"slope": [], "lag": [], "flat": [], "flat_lag": [], "naive": []}
    
    for end in range(min_train, len(df) - horizon + 1, step):
        window = df.iloc[:end]
        actual = df["weight"].iloc[end:end + horizon].to_numpy()
        
        trend = ewma_trend(window, halflife)
        rate = weekly_rate(trend, window["day"], span) / 7
        lag = halflife / np.log(2)
        
        preds = {
            "slope": ewma_forecast(window, horizon, halflife, span),
            "lag": ewma_forecast_lag(window, horizon, halflife, span),
            "flat": trend.iloc[-1],
            "flat_lag": trend.iloc[-1] + rate * lag,
            "naive": window["weight"].iloc[-1],
        }
        for name, pred in preds.items():
            scores[name].append(np.abs(actual - pred).mean())
    
    out = {name: np.mean(vals) for name, vals in scores.items()}
    out["runs"] = len(scores["naive"])
    
    return out

# Change this number for halflives
for hl in (0.5, 1, 2, 3, 5):
    for span in (14, 21):
        r = backtest_ewma(df, hl, span)
        print(f"hl {hl}d, span {span}: slope {r['slope']:.2f} | lag {r['lag']:.2f} | "
              f"flat {r['flat']:.2f} | flat_lag {r['flat_lag']:.2f} | naive {r['naive']:.2f} | runs {r['runs']}")
        
plt.scatter(df["modayr"], df["weight"], s = 8, c = "r", label = "Weight")
plt.plot(df["modayr"], df["ewma"], c = "b", label = "EWMA trend")
plt.legend()
plt.show()


# Previous Test Data

def load_user(path):
    d = pd.read_csv(path, parse_dates= ["modayr"])
    d = d.sort_values("modayr").reset_index(drop=True)
    d["day"] = (d["modayr"] - d["modayr"].min()).dt.days
    
    return d

users = [load_user(p) for p in sorted(glob.glob(r"data/training/user_*.csv"))]


predictors = ["slope", "lag", "flat", "flat_lag"]

def grid_all(users, halflives, spans, horizons, **kwargs):
    rows = []
    for hl, span, h in product(halflives, spans, horizons):
        res = [backtest_ewma(u, hl, span, horizon = h, **kwargs) for u in users]
        row = {"horizon": h, "halflife": hl, "span": span}
        
        for name in predictors + ["naive"]:
            row[name] = np.mean([r[name] for r in res])
        for name in predictors:
            row[name + "_wins"] = sum(r[name] < r["naive"] for r in res)
        
        rows.append(row)
    
    return pd.DataFrame(rows)


results = grid_all(users, halflives = (2,3,5), spans = (14, 28), horizons = (7,14), min_train = 90, step = 5)
for h, g in results.groupby("horizon"):
    print(f"\nHorizon {h} days")
    print(g.drop(columns = "horizon").round(3).sort_values("flat_lag").to_string(index = False))

print("done!")