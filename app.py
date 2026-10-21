# This is the dash board for the app

from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from Functions.plots import build_all
from Functions.analysis import raw_df, clean_df, recent_df
from Functions.classes import Measures
from data.key import secret_key


# looks for templates/ and static/ next to this file
app = Flask(__name__) 
app.secret_key = secret_key

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/weigh-in", methods = ["GET", "POST"])

def weigh_in():
    if request.method == "POST":
        f = request.form
        try:
            y, m, d = f["date"].split("-")
            Measures(float(f["weight"]), f"{m}/{d}/{y}", int(f["carb"]), int(f["fat"]),
                int(f["prot"]), int(f["cal"]), int(f["steps"]), int(f["activ"])).record()
        except (ValueError, KeyError) as e:
            flash(f"Could not save: {e}")
            return redirect(url_for("weigh_in"))
        flash("Weigh-in saved.")
        return redirect(url_for("recent"))
    
    
    return render_template("weigh_in.html")

@app.route("/analysis")

def analysis():
    return render_template("analysis.html")

@app.route("/analysis/raw")

def analysis_raw():
    return render_template("data_table.html", title = "Raw data", df = raw_df())

@app.route("/analysis/cleaned")

def analysis_cleaned():
    return render_template("data_table.html", title = "Cleaned data", df = clean_df())

@app.route("/analysis/review")

def dashboard():
    source = request.args.get("source", "cleaned")
    
    if source == "raw":
        df = raw_df()
        df["modayr"] = pd.to_datetime(df["modayr"], errors="coerce")
        df = df.dropna().sort_values("modayr").reset_index(drop=True)
    else:
        source = "cleaned"
        clean_df()
        df = None
    
    plots = {name: fig.to_html(full_html=False, include_plotlyjs=False) for name, fig in build_all(df).items()}
    
    
    return render_template("dashboard.html", plots=plots, source=source)


@app.route("/recent")

def recent():
    return render_template("data_table.html", title = "Recent weigh-ins (last 7)", df = recent_df("raw"))


if __name__ == "__main__":
    app.run(debug=True)