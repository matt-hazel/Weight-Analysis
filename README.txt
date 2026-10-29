WEIGHT TRACKER
==============

A small Flask web app for tracking a weight loss (or gain) journey. You log
daily weigh-ins along with calories, macros, steps and activity, and the
dashboard charts your progress and forecasts where your weight is heading.


WHAT IT DOES
------------
- Weigh-in form: record weight, date, carbs, fat, protein, calories, steps
  and activity level.
- Recent weigh-ins: the last 7 entries.
- Data views: the raw CSV and the cleaned version.
- Dashboard (Scientific Analysis > Review): weight forecast, weight vs
  intake and activity, calories vs weight, weekly heatmap and correlations.


REQUIREMENTS
------------
Python 3.11 or newer (developed on 3.14) with:

    numpy, pandas, flask, plotly, statsmodels

statsmodels is needed for the trendline on the "Calories vs weight" chart.
Install dependencies with "pip install -r requirements.txt"


SETUP
-----
1. Create the secret key file the app imports (data/ is not tracked by git):

       data/key.py
           secret_key = "any long random string"

2. Run from the project root (file paths are relative to it):

       python main.py

   The app opens at http://127.0.0.1:5000/.

data/weight.csv is created the first time you save a weigh-in.
data/weight_clean.csv is rebuilt from it whenever the cleaned data is viewed.


PROJECT LAYOUT
--------------
    main.py                 Launches the app and opens the browser
    app.py                  Flask routes
    Functions/
        classes.py          Measures: validates and saves a weigh-in
        data_pipe.py        Cleaning pipeline (schema, range checks, fixes)
        analysis.py         Loads raw/cleaned/recent data
        plots.py            Dashboard charts (Plotly)
        forecast.py         Forecast model used by the dashboard
        model.py            Backtesting and tuning experiments (not used by the app)
    templates/, static/     HTML and CSS
    data/                   Your data (git-ignored)


THE FORECAST MODEL
------------------
Daily weight is noisy (about +/- 1 lb from water alone), so the model works
on a smoothed trend:

1. EWMA trend. An exponentially weighted moving average (half-life 5 days)
   smooths daily fluctuations. It is time-aware, so missed days are handled
   correctly.
2. Rate of change. A straight line fitted to the last 28 weigh-ins of the
   trend gives your current rate in lbs per day.
3. Lag correction. A moving average trails behind a falling series by about
   half-life / ln(2) days. The rate is multiplied by that delay and added
   back, which puts the trend where you probably are now.
4. Damped forecast. The forecast continues from the corrected level along
   the current rate, with the daily change shrinking by a factor of 0.9 each
   day (damping). The line bends toward a plateau instead of dropping
   forever.

Settings live at the top of Functions/forecast.py (half-life, span, damping,
horizon, minimum rows). At least 14 weigh-ins are needed before a forecast
is shown.

How it was chosen
-----------------
Settings were tuned with rolling-origin backtests on 30 sample datasets of
730 days each: train on the past, forecast the next 7 or 14 days, slide
forward, and compare against "tomorrow equals today's weight".

    Average error (lbs)     7 days    14 days
    Last weigh-in (naive)    0.897     0.965
    This model, damped       0.775     0.825

That is roughly 14% lower error, and the model beat the naive baseline for
29-30 of 30 users. Earlier attempts (linear and polynomial regression) were
rejected: they fit the past but diverge when extended forward.

Limits
------
- Average error is about 0.8 lb. Much of this is daily noise no weight-only
  model can predict.
- The sample datasets lose weight slowly (about 0.5 lb/week). Settings have
  not been validated on a long history of real data.
- The forecast uses weight only. Calories and steps are charted but not yet
  used in the prediction.
- No uncertainty range is shown yet.
- Damping (0.9) was the best value tested, not a proven optimum.


DATA FORMAT
-----------
weight.csv columns: weight, modayr (M/D/YYYY), carb, fat, prot, cal, steps, activ

Cleaning rules (Functions/data_pipe.py): values outside the allowed range
become missing, missing weights are interpolated, rows missing other
required fields are dropped, and duplicate dates are removed.


RUNNING THE EXPERIMENTS
-----------------------
Functions/model.py contains the backtests and the grid search across
data/training/user_*.csv. The training folder is git-ignored, so supply
your own files with the same columns to rerun it.


ROADMAP
-------
- Forecast uncertainty band and headline numbers on the dashboard
- Use calories and steps as drivers of weight change
- Replace the automatic package installer with requirements.txt