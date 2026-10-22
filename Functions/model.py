# Linear Regression model set up for weight trend prediction

from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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

X_train, X_test, y_train, y_test = train_test_split(X, y)

split = int(len(df) * 0.8)
train, test = df.iloc[:split], df.iloc[split:]

model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)




#plotting


plt.scatter(df['modayr'], y, c ='r')
plt.plot(df['modayr'], y, c ='b')
plt.plot(X_test, y_pred, c = 'g')
plt.show()