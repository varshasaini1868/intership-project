from flask import Flask, render_template
from sheet_database import get_devices_for_dashboard




import threading
import time
import webbrowser
import os

scan_network = None

if os.getenv("RUN_SCANNER", "true").lower() == "true":
    from scanner import scan_network
app = Flask(__name__)


# Background Auto Scanner
def auto_scan():
   if scan_network is None:
    return
    while True:

        print("Scanning Network...")

        try:
            scan_network()

        except Exception as e:
            print("Scan Error:", e)

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

if scan_network is not None:

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