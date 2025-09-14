from flask import Flask, render_template, jsonify
from db.db_utils import get_latest_readings
from datetime import datetime
import pytz

app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def dashboard():
    readings = get_latest_readings()
    tz = pytz.timezone("Pacific/Auckland")
    current_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    return render_template("dashboard.html", readings=readings, current_time=current_time)

@app.route("/api/readings")
def api_readings():
    readings = get_latest_readings()
    return jsonify(readings)

if __name__ == "__main__":
    app.run(debug=True)
