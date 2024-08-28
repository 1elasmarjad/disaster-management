from flask import Flask, render_template

from data import EarthquakeUSGS, WildfiresNASA, OLDEST_DATA

app = Flask(__name__)


@app.route('/api/data')
def fetch_api_data():
    usgs = EarthquakeUSGS()
    earthquakes = usgs.get_data()

    nasa = WildfiresNASA()
    wildfires = nasa.get_data()

    return {
        "disasters": list(earthquakes) + list(wildfires),
    }


@app.route('/')
def index():
    return render_template("index.html", oldest_data=OLDEST_DATA.days)


if __name__ == '__main__':
    app.run()
