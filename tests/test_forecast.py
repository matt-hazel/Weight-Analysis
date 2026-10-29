# this is for the testing of the forecasting model, ensuring correct inputs of df


import pandas as pd

from Functions.forecast import forecast, MIN_ROWS

def make_df(n, start = 200.0, step = -0.1):
    return pd.DataFrame({
        "modayr": pd.date_range("2026-01-01", periods = n),
        "weight": [start + step * i for i in range(n)]
    })
    
def test_too_little_data_returns_none():
    assert forecast(make_df(MIN_ROWS - 1)) is None
    

def test_losing_weight_gives_neg():
    result = forecast(make_df(30))
    
    assert result["weekly_rate"] < 0
    
    
def test_forecast_length_match_hori():
    result = forecast(make_df(30), horizon = 10)
    
    assert len(result["future"]) == 10
    assert len(result["dates"]) == 10