from flask import Flask, render_template
from sheet_database import get_devices_for_dashboard

app = Flask(__name__)


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


@app.route("/planner")
def planner():
    return render_template("planner.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)