# Linear Regression model was not of good fit. Attempting Polynomial Regression

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# load data

df = pd.read_csv(r"data/training/user_01.csv", parse_dates = ['modayr'])
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

model = LinearRegression()
model.fit(train[["day"]], train["weight"])

test_pred = model.predict(test[["day"]])
mae = np.abs(test["weight"] - test_pred).mean()
print(f"Slope: {model.coef_[0] * 7:.2f} lbs/week | Test MAE: {mae:.2f} lbs")


#plotting

df["trend"] = model.predict(df[["day"]])

plt.scatter(df["modayr"], df["weight"], c="r", label = "Weight")
plt.plot(df["modayr"], df["trend"], c = "g", label = "Linear trend")
plt.axvline(test["modayr"].iloc[0], c = "gray", ls = "--", label = "Train/Test split")
plt.legend()
plt.show()