import urllib
from abc import ABC, abstractmethod
import urllib.parse
from datetime import datetime, timedelta
from typing import Generator

import requests

from proj_types.thirdparty_api import EarthquakeFetchData, NASAEventsFetchData
from proj_types.provider_api import Disaster

OLDEST_DATA = timedelta(days=12)

MIN_LATITUDE = 24.6
MAX_LATITUDE = 50
MIN_LONGITUDE = -125
MAX_LONGITUDE = -65


class ThirdPartyData(ABC):

    def __init__(self, url: str, query_params: dict, headers: dict = None):
        self.url = url
        self.query_params = query_params
        self.headers = headers

    def __make_request(self):
        gen_url = self.url if not self.query_params else self.url + "?" + urllib.parse.urlencode(self.query_params)
        return requests.get(gen_url, headers=self.headers)

    @abstractmethod
    def handle_request(self, response: requests.Response) -> list[Disaster]:
        raise NotImplementedError

    def get_data(self) -> list[Disaster]:
        response = self.__make_request()
        return self.handle_request(response)


class EarthquakeUSGS(ThirdPartyData):

    def __init__(self):
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

        current_date = datetime.now()
        start_time = current_date - OLDEST_DATA

        params = {
            "format": "geojson",
            "starttime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "minlatitude": MIN_LATITUDE,
            "maxlatitude": MAX_LATITUDE,
            "minlongitude": MIN_LONGITUDE,
            "maxlongitude": MAX_LONGITUDE,
        }

        super().__init__(url, params)

    def handle_request(self, response: requests.Response) -> Generator[Disaster, None, None]:
        data: EarthquakeFetchData = response.json()

        for feature in data["features"]:
            yield {
                "type": "earthquake",
                "geometry": feature["geometry"],
                "metadata": feature["properties"]
            }


class WildfiresNASA(ThirdPartyData):

    def __init__(self):
        url = "https://eonet.gsfc.nasa.gov/api/v2.1/events"

        params = {
            "days": OLDEST_DATA.days,
        }

        super().__init__(url, params)

    def handle_request(self, response: requests.Response) -> list[Disaster]:
        data: NASAEventsFetchData = response.json()

        for event in data["events"]:
            is_wildfire = any(category["id"] == 8 for category in event["categories"])

            if not is_wildfire:
                continue

            if event["geometries"][0]["type"] != "Point":
                continue

            point = event["geometries"][0]["coordinates"]

            lat = point[1]
            lon = point[0]

            # not in the US?
            if not (MIN_LATITUDE <= lat <= MAX_LATITUDE and MIN_LONGITUDE <= lon <= MAX_LONGITUDE):
                continue

            yield {
                "type": "wildfire",
                "geometry": {
                    "type": "Point",
                    "coordinates": point,
                },
                "metadata": {
                    "title": event["title"],
                    "description": event["description"],
                }
            }
