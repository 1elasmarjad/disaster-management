import urllib
from abc import ABC, abstractmethod
import urllib.parse
from datetime import datetime, timedelta
from typing import Generator

import requests

from proj_types.thirdparty_api import EarthquakeFetchData, NASAEventsFetchData
from proj_types.provider_api import Disaster

OLDEST_DATA = timedelta(days=7)

MIN_LATITUDE = 24.6
MAX_LATITUDE = 50
MIN_LONGITUDE = -125
MAX_LONGITUDE = -65

FETCH_CACHE: dict[str, dict] = {}  # takes a url and returns a json/dict response of the data


class ThirdPartyData(ABC):

    def __init__(self, url: str, query_params: dict):
        self.url = url
        self.query_params = query_params

    def __make_request(self) -> dict:
        gen_url = self.url if not self.query_params else self.url + "?" + urllib.parse.urlencode(self.query_params)

        cached_data = FETCH_CACHE.get(gen_url)  # check if the data is already fetched and return it if it is

        if cached_data:
            return cached_data

        data_response = requests.get(gen_url).json()
        FETCH_CACHE[gen_url] = data_response

        return data_response

    @abstractmethod
    def handle_request(self, data: dict) -> list[Disaster]:
        raise NotImplementedError

    def get_data(self) -> list[Disaster]:
        response: dict = self.__make_request()
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

    def handle_request(self, data: EarthquakeFetchData) -> Generator[Disaster, None, None]:
        for feature in data["features"]:
            yield {
                "type": "earthquake",
                "geometry": feature["geometry"],
                "metadata": feature["properties"]
            }


class NASAEvents(ThirdPartyData, ABC):

    def __init__(self, event_id: int, event_type: str, us_only: bool = True):
        self.event_id = event_id
        self.event_type = event_type
        self.us_only = us_only

        super().__init__("https://eonet.gsfc.nasa.gov/api/v2.1/events", {
            "days": OLDEST_DATA.days,
        })

    def handle_request(self, data: NASAEventsFetchData) -> list[Disaster]:

        for event in data["events"]:
            is_target_event = any(category["id"] == self.event_id for category in event["categories"])

            if not is_target_event:
                continue

            if event["geometries"][0]["type"] != "Point":
                continue

            point = event["geometries"][0]["coordinates"]

            lat = point[1]
            lon = point[0]

            # not in the US?
            if self.us_only and not (MIN_LATITUDE <= lat <= MAX_LATITUDE and MIN_LONGITUDE <= lon <= MAX_LONGITUDE):
                continue

            yield {
                "type": self.event_type,
                "geometry": {
                    "type": "Point",
                    "coordinates": point,
                },
                "metadata": {
                    "title": event["title"],
                    "description": event["description"],
                }
            }


class WildfiresNASA(NASAEvents):

    def __init__(self):
        super().__init__(8, "wildfire")


class StormsNASA(NASAEvents):

    def __init__(self):
        super().__init__(10, "storm", us_only=False)
