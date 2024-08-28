import urllib
from abc import ABC, abstractmethod
import urllib.parse
from datetime import datetime, timedelta
from typing import Generator

import requests

from proj_types.earthquake_api import EarthquakeFetchData
from proj_types.provider_api import Disaster


class ThirdPartyData(ABC):

    def __init__(self, url: str, query_params: dict):
        self.url = url
        self.query_params = query_params

    def __make_request(self):
        gen_url = self.url if not self.query_params else self.url + "?" + urllib.parse.urlencode(self.query_params)
        return requests.get(gen_url)

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
        start_time = current_date - timedelta(days=1)

        params = {
            "format": "geojson",
            "starttime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "minlatitude": 24.6,
            "maxlatitude": 50,
            "minlongitude": -125,
            "maxlongitude": -65,
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
