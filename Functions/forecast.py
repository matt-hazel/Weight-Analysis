# This is the set up for the EWMA + Lag correction forecasting model for the dashboard.

import numpy as np
import pandas as pd

halflife = 5
span = 28
horizon = 14
min_rows = 14



def prepare(df):
    # double checking data for cleanleness (i think i spelled that right, im losing it lol)
    
    d = df[["modayr", "weight"]].dropna().drop_duplicates("modayr")
    d = d.sort_values("modayr").reset_index(drop = True)
    d["day"] = (d["modayr"] - d["modayr"].min()).dt.days
    
    
    return d


def ewma_trend(d, halflife = halflife):
    return d["weight"].ewm(halflife = f"{halflife} days", times = d["modayr"]).mean()


def daily_rate(trend, days, span = span):
    span = min(span, len(trend))
    
    
    return np.polyfit(days.iloc[-span:], trend.iloc[-span:], 1)[0]


def forecast(df, horizon = horizon, halflife = halflife, span = span):
    d = prepare(df)
    if len(d) < min_rows:
        return None # setup display on dash to say like "unlock prediction at 14 days"
    
    d["trend"] = ewma_trend(d, halflife)
    
    rate = daily_rate(d["trend"], d["day"], span)
    
    level = d["trend"].iloc[-1] + rate * halflife / np.log(2)
    
    dates = pd.date_range(d["modayr"].iloc[-1] + pd.Timedelta(days = 1), periods = horizon)
    
    
    return {"data": d, "level": level, "weekly_rate": rate * 7, "dates": dates}