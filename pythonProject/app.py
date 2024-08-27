from datetime import datetime, timedelta

from flask import Flask
import requests
import urllib.parse

from proj_types.earthquake_api import EarthquakeFetchData

app = Flask(__name__)

DATA_FRESHNESS = timedelta(days=7)


@app.route('/api/data')
def fetch_api_data():
    url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    current_date = datetime.now()
    start_time = current_date - DATA_FRESHNESS

    params = {
        "format": "geojson",
        "starttime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
    }

    resp = requests.get(url + "?" + urllib.parse.urlencode(params))
    data: EarthquakeFetchData = resp.json()

    return data


if __name__ == '__main__':
    app.run()
