# This isn't going to be truly implemented in final product.
# This is just toying with which plots would be the best case scenario for the data I have.

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

data = pd.read_csv(r"data\weight_clean.csv")
data["modayr"] = pd.to_datetime(data["modayr"], errors="coerce")
data["day_num"] = (data["modayr"]).dt.day

print("Data Review")
print("---------------------------------------------------")
print("Data Header")
print(data.head())
print("---------------------------------------------------")
print("Data Tail")
print(data.tail())
print("---------------------------------------------------")
print("Data Info")
print(data.info())
print("---------------------------------------------------")
print("Data Description")
print(data.describe())
print("---------------------------------------------------")


fig = px.scatter_matrix(data, 
                        dimensions=["weight", "carb", "fat", "prot", "cal", "steps", "activ","modayr"], 
                        color="modayr",title="Scatter Matrix of Weight Data",
                        labels={"modayr":"Date of Weigh-in"})
fig.update_traces(diagonal_visible=False)
fig.show()

df = pd.read_csv(r"data\weight_clean.csv", parse_dates=["modayr"])

corr = df.drop(columns=["modayr"]).corr()
fig1 = px.imshow(
    corr,
    text_auto=".2f",
    color_continuous_scale="RdBu_r",
    title="Correlation Heatmap of Weight Data",
    labels={"x": "Features", "y": "Features", "color": "Correlation"},
)

fig1.show()

df["week"] = df["modayr"].dt.to_period("W").dt.start_time
df["dow"] = df["modayr"].dt.day_name()

order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

pivot = df.pivot(index = "week", columns = "dow", values = "weight")[order]
fig2 = px.imshow(pivot, text_auto = ".0f", color_continuous_scale="YlOrRd", aspect = "auto")
fig2.show()

df = pd.read_csv(r"data\weight_clean.csv", parse_dates=["modayr"])

for c in ["weight", "cal", "steps"]:
    # for smoothing daily noise
    df[c + "_7d"] = df[c].rolling(7, min_periods=3).mean()

fig3 = make_subplots(rows = 3, cols = 1, shared_xaxes = True,
                     subplot_titles = ("Weight (lb)", "Calories", "Steps"))

fig3.add_scatter(x = df.modayr, y = df.weight, mode = "markers", opacity = 0.4, row = 1, col = 1, name = "weight")
fig3.add_scatter(x = df.modayr, y = df.weight_7d, row = 1, col = 1, name = "weight 7d avg")
fig3.add_scatter(x = df.modayr, y = df.cal_7d, row = 2, col = 1, name = "cal 7d avg")
fig3.add_scatter(x = df.modayr, y = df.steps_7d, row = 3, col = 1, name = "steps 7d avg")
fig3.update_layout(height = 800, title = "Weight vs intake and Activity")

fig3.show()

fig4 = px.scatter(df, x = "cal_7d", y = "weight_7d", trendline = "ols", trendline_scope = "overall", trendline_color_override="darkblue", color = "modayr")
fig4.update_yaxes(autorange="reversed")
fig4.show()

fig6 = px.line(data, x = "modayr", y = "weight", markers = True, title = "Weight tracking over time")
fig6.show()