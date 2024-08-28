from datetime import datetime, timedelta

from flask import Flask, render_template
import requests
import urllib.parse

from proj_types.earthquake_api import EarthquakeFetchData

app = Flask(__name__)

DATA_FRESHNESS = timedelta(days=7)  # how fresh the data from apis should be


@app.route('/api/data')
def fetch_api_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    current_date = datetime.now()
    start_time = current_date - DATA_FRESHNESS

    params = {
        "format": "geojson",
        "starttime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
        "minlatitude": 24.6,
        "maxlatitude": 50,
        "minlongitude": -125,
        "maxlongitude": -65,
    }

    resp = requests.get(url + "?" + urllib.parse.urlencode(params))
    data: EarthquakeFetchData = resp.json()

    return data


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
