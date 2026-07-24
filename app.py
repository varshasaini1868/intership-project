from flask import Flask, render_template
from sheet_database import get_devices_for_dashboard
from scanner import scan_network

import threading
import time
import webbrowser

app = Flask(__name__)


# Background Auto Scanner
def auto_scan():

    while True:

        print("Scanning Network...")

        try:
            scan_network()

        except Exception as e:
            print("Scan Error:", e)

        # 30 sec me ek baar scan
        time.sleep(30)


# Dashboard Route
@app.route("/")
def home():

    data = get_devices_for_dashboard()

    return render_template(
        "dashboard.html",
        total=data["total"],
        online=data["online"],
        offline=data["offline"],
        health=data["health"],
        avg_latency=data["avg_latency"],
        devices=data["devices"]
    )
def planner():

    return render_template(
        "planner.html"
    )


# Background Scanner Thread
import os

if os.environ.get("RENDER") is None:

    scanner_thread = threading.Thread(
        target=auto_scan,
        daemon=True
    )

    scanner_thread.start()

# Run Flask App
if __name__ == "__main__":

   if os.environ.get("RENDER") is None:
    try:
        webbrowser.open("http://localhost:5000")
    except:
        pass

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )