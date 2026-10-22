# Linear Regression model was not of good fit. Attempting Polynomial Regression

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression

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
y = df['weight']

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

df["trend"] = model.predict(df[["day"]])

plt.scatter(df["modayr"], df["weight"], s=8, c="r", label="Weight")
plt.plot(df["modayr"], df["fit"], c="g", label=f"Polynomial (degree {best})")
plt.axvline(test["modayr"].iloc[0], c="gray", ls="--", label="Train/test split")
plt.legend()
plt.show()