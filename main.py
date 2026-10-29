# The point of this program is to create something that can help assist my weight loss journey.
# It will hold onto data inputs in a CSV, which will also be used as a source to track trends via D.S.

import threading
import webbrowser

from app import app

URL = "http://127.0.0.1:5000/"


def main():
    threading.Timer(1.0, lambda: webbrowser.open_new(URL)).start()
    app.run(debug=False)    


if __name__ == "__main__":
    main()