# This is the dash board for the app

from flask import Flask, render_template, request, url_for, jsonify, abort
from Functions.plots import build_all


# looks for templates/ and static/ next to this file
app = Flask(__name__) 

@app.route("/")
def menu():
    return render_template("menu.html")

@app.route("/weigh-in")

def weigh_in():
    return render_template("weigh_in.html")

@app.route("/analysis")

def analysis():
    return render_template("analysis.html")

@app.route("/analysis/raw")

def analysis_raw():
    return render_template("analysis/raw.html")

@app.route("analysis/cleaned")

def analysis_cleaned():
    return render_template("analysis/cleaned.html")

@app.route("/analysis/review")

def analysis_review():
    return render_template("analysis/review.html")


@app.route("/dashboard")

def dashboard():
    plots = {name: fig.to_html(full_html = False, include_plotlyjs = False)
             for name, fig in build_all().items()}

    return render_template("dashboard.html", plots = plots)


if __name__ == "__main__":
    app.run(debug=True)