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

print(df.head())
print(df.tail())

# init

X = df[['day']]
y = df['weight'] # DELETE THESE

# modelling

split = int(len(df) * 0.8)
train = df.iloc[:split]
test = df.iloc[split:]

naive_mae = np.abs(test["weight"] - train["weight"].iloc[-1]).mean()
print(f"Naive MAE: {naive_mae:.2f} lbs")

results = {}

for degree in (1,2,3,4,5):
    model = make_pipeline(
        StandardScaler(),
        PolynomialFeatures(degree),
        LinearRegression(),
    )
    model.fit(train[["day"]], train["weight"])
    pred = model.predict(test[["day"]])
    mae = np.abs(test["weight"] - pred).mean()
    results[degree] = (model, mae)
    print(f"Degree {degree}: test MAE {mae:.2f} lbs")
    
best = min(results, key = lambda d: results[d][1])
    
print(f"Best degree: {best}")
    
df["fit"] = results[best][0].predict(df[["day"]])


#plotting

df["trend"] = model.predict(df[["day"]]) # DELETE

plt.scatter(df["modayr"], df["weight"], s=8, c="r", label="Weight")
plt.plot(df["modayr"], df["fit"], c="g", label=f"Polynomial (degree {best})")
plt.axvline(test["modayr"].iloc[0], c="gray", ls="--", label="Train/test split")
plt.legend()
plt.show()


def plateau(t, floor, drop, k):
    return floor + drop * np.exp(-k * t)

def fit_plateau(window):
    # the window is last N rows of the dataframe
    
    t = window["day"] - window["day"].iloc[0]
    w = window["weight"]
    p0 = [w.iloc[-1], w.iloc[0] - w.iloc[-1], 0.02]
    params, _ = curve_fit(plateau, t, w, p0=p0, bounds = ([0, -200, 0], [500, 200, 1]), maxfev = 5000)
    
    return params

def forecast(window, horizon = 14):
    params = fit_plateau(window)
    t0 = window["day"].iloc[0]
    future = np.arange(window["day"].iloc[-1] + 1, window["day"].iloc[-1] + 1 + horizon)
    
    return future, plateau(future - t0, *params)

def backtest(df, max_window, horizon = 14, step = 7):
    errs, naive_errs = [],[]
    
    for end in range(max_window, len(df) - horizon, step):
        window = df.iloc[max(0, end - max_window):end]
        actual = df.iloc[end:end + horizon]
        
        try:
            params = fit_plateau(window)
        except RuntimeError:
            continue
        
        t0 = window["day"].iloc[0]
        pred = plateau(actual["day"] - t0, *params)
        errs.append(np.abs(actual["weight"] - pred).mean())
        naive_errs.append(np.abs(actual["weight"] - window["weight"].iloc[-1]).mean())
    
    return np.median(errs), np.median(naive_errs), len(errs)
    
    
    
    
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