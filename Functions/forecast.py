# This is the set up for the EWMA + Lag correction forecasting model for the dashboard.

import numpy as np
import pandas as pd

HALFLIFE = 5
SPAN = 28
HORIZON = 21 # prediction horizon
MIN_ROWS = 14 # min amount of data to be used
PHI = 0.9 # dampening factor



def prepare(df):
    # double checking data for cleanleness (i think i spelled that right, im losing it lol)
    
    d = df[["modayr", "weight"]].dropna().drop_duplicates("modayr")
    d = d.sort_values("modayr").reset_index(drop = True)
    d["day"] = (d["modayr"] - d["modayr"].min()).dt.days
    
    
    return d


def ewma_trend(d, halflife = HALFLIFE):
    return d["weight"].ewm(halflife = f"{halflife} days", times = d["modayr"]).mean()



def local_rate(trend, days, span = SPAN):
    # This is for the slope of the pre-forecasted line.
    
    t, x = trend.to_numpy(), days.to_numpy()
    out = np.zeros(len(t))
    
    for i in range(2, len(t)):
        lo = max(0, i + 1 - span)
        out[i] = np.polyfit(x[lo:i + 1], t[lo:i + 1], 1)[0]
        
    return out


def forecast(df, horizon = HORIZON, halflife = HALFLIFE, span = SPAN, phi = PHI):
    d = prepare(df)
    if len(d) < MIN_ROWS:
        return None
    
    d["trend"] = ewma_trend(d, halflife)
    d["rate"] = local_rate(d["trend"], d["day"], span)
    d["smooth"] = d["trend"] + d["rate"] * halflife / np.log(2)
    
    level = d["smooth"].iloc[-1]
    rate = d["rate"].iloc[-1]
    steps = np.arange(1, horizon + 1)
    future = level + rate * np.cumsum(phi ** steps)
    dates = pd.date_range(d["modayr"].iloc[-1] + pd.Timedelta(days = 1), periods = horizon)
    
    return {"data": d, "level": level, "future": future, "weekly_rate": d["rate"].iloc[-1] * 7, "dates": dates}