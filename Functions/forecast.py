# This is the set up for the EWMA + Lag correction forecasting model for the dashboard.

import numpy as np
import pandas as pd



FEATURES = ["cal", "steps", "activ"]
FEAT_HALFLIFE = 4
LAM = 5 # ridge penality
MIN_FIT_ROWS = 28
MAX_SHIFT = 0.5 / 7 # habits change rate, lb/day

HALFLIFE = 5
SPAN = 28
HORIZON = 21 # prediction horizon
MIN_ROWS = 14 # min amount of data to be used
PHI = 0.9 # dampening factor



def prepare(df):
    # double checking data for cleanleness (i think i spelled that right, im losing it lol)
    
    d = df[["modayr", "weight", *FEATURES]].dropna().drop_duplicates("modayr")
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

def fit_intake_model(d, feats = FEATURES, hl = FEAT_HALFLIFE, lam = LAM):
    # this function learns how smooth the daily weight change responds to activity and consumption

    w = d["weight"].ewm(halflife = f"{hl} days", times = d["modayr"]).mean()
    dw = (w.diff() / d["day"].diff()).iloc[1:].to_numpy()

    F = d[feats].ewm(halflife = f"{hl} days", times = d["modayr"]).mean()
    X = F.iloc[1:].to_numpy()

    mu, sd = X.mean(axis = 0), X.std(axis = 0) + 1e-9
    Z = (X - mu) / sd
    b = np.linalg.solve(Z.T @ Z + lam * np.eye(Z.shape[1]), Z.T @ (dw - dw.mean()))


    return {"sd": sd, "b": b, "F": F.to_numpy()}


def habit_shift(m, span = SPAN):
    now = m["F"][-1] #smoothed habits today
    ref = m["F"][-span:].mean(axis = 0) # typical smoothed habits over the span behind slope
    delta = ((now - ref) / m["sd"]) @ m["b"]


    return float(np.clip(delta, -MAX_SHIFT, MAX_SHIFT))


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
    
    shift = habit_shift(fit_intake_model(d)) if len(d) >= MIN_FIT_ROWS else 0.0
    future = level + np.cumsum((rate + shift) * phi ** steps)
        
    dates = pd.date_range(d["modayr"].iloc[-1] + pd.Timedelta(days = 1), periods = horizon)
    
    return {"data": d, "level": level, "future": future, "weekly_rate": d["rate"].iloc[-1] * 7, "dates": dates, "shift_weekly": shift * 7}