# This is the recreation of data_review.py from the data expo phase.
# The plots that are created here are to be put into the dashboard for data analysis for the user.

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

clean_csv = Path(__file__).resolve().parent.parent / "data" / "weight_clean.csv"
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def load_data():
    df = pd.read_csv(clean_csv, parse_dates=["modayr"])
    df["modayr"] = pd.to_datetime(df["modayr"], errors = "coerce")
    
    return df.sort_values("modayr").reset_index(drop=True)

def add_rolling(df, cols = ("weight", "cal", "steps"), window = 7):
    # This returns a copy with (col)7d smooth columns
    
    out = df.copy()
    
    for c in cols:
        out[f"{c}_7d"] = out[c].rolling(window, min_periods = 3).mean()
    
    return out

def weight_over_time(df):
    return px.line(df, x = "modayr", y = "weight", markers = True, title = "Weight tracking over time")

def scatter_matrix(df):
    fig = px.scatter_matrix(
        df,
        dimensions = ["weight", "carb", "fat", "prot", "cal", "steps", "activ", "modayr"],
        color = "modayr",
        title = "Scatter Matrix of Weight Data",
        labels = {"modayr": "Date of Weigh-in"}
    )
    
    fig.update_traces(diagonal_visible = False)
    
    return fig


def correlation_heatmap(df):
    corr = df.drop(columns = ["modayr"]).corr(numeric_only = True)
    
    return px.imshow(
        corr,
        text_auto = ".2f",
        color_continuous_scale = "RdBu_r",
        title = "Correlation Heatmap of Weight Data",
        labels = {"x": "Features", "y": "Features", "color": "Correlation"}
    )
    

def weekly_heatmap(df):
    d = df.copy()
    d["week"] = d["modayr"].dt.to_period("W").dt.start_time
    d["dow"] = d["modayr"].dt.day_name()
    
    # Pivot table and reindex tolerates dup. days and missing weekdays
    
    pivot = (d.pivot_table(index = "week", columns = "dow", values = "weight", aggfunc = "mean").reindex(columns = dow_order))
    
    return px.imshow(pivot, text_auto = ".0f", color_continuous_scale = "YlOrRd", aspect = "auto", title = "Weight by week and weekday")


def weight_vs_intake_activity(df):
    d = add_rolling(df)

    fig = go.Figure()
    fig.add_scatter(x=d.modayr, y=d.weight, mode="markers", opacity=0.4, name="Weight")
    fig.add_scatter(x=d.modayr, y=d.weight_7d, mode="lines", name="Weight 7D Avg")
    fig.add_scatter(x=d.modayr, y=d.cal_7d, mode="lines", name="Calories 7D Avg", yaxis="y2")
    fig.add_scatter(x=d.modayr, y=d.steps_7d, mode="lines", name="Steps 7D Avg", yaxis="y3")

    fig.update_layout(
        height=600,
        title="Weight vs intake and Activity",
        xaxis=dict(title="Date", domain=[0, 0.85]),
        yaxis=dict(title="Weight (lb)"),
        yaxis2=dict(title="Calories", overlaying="y", side="right"),
        yaxis3=dict(title="Steps", overlaying="y", side="right", anchor="free", position=0.95),
    )
    return fig

def calories_vs_weight(df):
    d = add_rolling(df)
    
    fig = px.scatter(d, x = "cal_7d", y = "weight_7d", trendline = "ols",
                     trendline_scope = "overall", trendline_color_override='darkblue',
                     color = "modayr", title = "7 day calories vs 7 day weight"
                     )
    fig.update_yaxes(autorange = "reversed")
    
    return fig


# This is the order of the plots as they will be displayed on the dashboard (app.py)

plots = {
    "Weight over time": weight_over_time,
    "Weight vs intake + activity": weight_vs_intake_activity,
    "Calories vs weight": calories_vs_weight,
    "Weekly heatmap": weekly_heatmap,
    "Correlations": correlation_heatmap,
    "Scatter matrix": scatter_matrix
}

# This function builds everything

def build_all(df = None):
    # name to figure for every plot in "plots"
    
    df = load_data() if df is None else df
    
    return {name: fn(df) for name, fn in plots.items()}