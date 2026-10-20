# This is the dash board for the app

from flask import Flask, render_template, request, url_for, jsonify, abort
from Functions.plots import build_all


# looks for templates/ and static/ next to this file
app = Flask(__name__) 

@app.route("/")

def dashboard():
    plots = {name: fig.to_html(full_html = False, include_plotlyjs = False)
             for name, fig in build_all().items()}

    return render_template("dashboard.html", plots = plots)


if __name__ == "__main__":
    app.run(debug=True)