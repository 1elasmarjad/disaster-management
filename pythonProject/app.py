from flask import Flask, render_template

from data import EarthquakeUSGS, WildfiresNASA, OLDEST_DATA, StormsNASA

app = Flask(__name__)


@app.route('/api/data')
def fetch_api_data():
    earthquakes_usgs = EarthquakeUSGS()
    earthquakes = earthquakes_usgs.get_data()

    wildfires_nasa = WildfiresNASA()
    wildfires = wildfires_nasa.get_data()

    storms_nasa = StormsNASA()
    worldwide_storms = storms_nasa.get_data()

    return {
        "disasters": list(earthquakes) + list(wildfires) + list(worldwide_storms),
    }


@app.route('/')
def index():
    return render_template("index.html", oldest_data=OLDEST_DATA.days)


if __name__ == '__main__':
    app.run()
