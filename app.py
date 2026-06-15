from flask import Flask, render_template
from database import get_devices
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

    devices = get_devices()

    total = len(devices)

    online = sum(
        1 for device in devices
        if device["status"] == "Online"
    )

    offline = sum(
        1 for device in devices
        if device["status"] == "Offline"
    )

    # Network Health
    if total > 0:
        health = round(
            (online / total) * 100,
            2
        )
    else:
        health = 0

    # Average Latency
    online_devices = [
        device
        for device in devices
        if device["status"] == "Online"
    ]

    if len(online_devices) > 0:

        avg_latency = round(
            sum(
                device["latency"]
                for device in online_devices
            )
            /
            len(online_devices),
            2
        )

    else:
        avg_latency = 0

    return render_template(
        "dashboard.html",
        total=total,
        online=online,
        offline=offline,
        health=health,
        avg_latency=avg_latency,
        devices=devices
    )


# Station Planning Simulator
@app.route("/planner")
def planner():

    return render_template(
        "planner.html"
    )


# Background Scanner Thread
scanner_thread = threading.Thread(
    target=auto_scan,
    daemon=True
)

scanner_thread.start()


# Run Flask App
if __name__ == "__main__":

    try:
        webbrowser.open(
            "http://localhost:5000"
        )
    except:
        pass

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )