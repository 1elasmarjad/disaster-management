from flask import Flask, render_template

from data import EarthquakeUSGS

app = Flask(__name__)


@app.route('/api/data')
def fetch_api_data():
    usgs = EarthquakeUSGS()
    data = usgs.get_data()

    return {
        "features": list(data),
    }


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
