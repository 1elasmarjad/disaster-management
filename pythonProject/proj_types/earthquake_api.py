from typing import TypedDict, Literal


class FeatureGeometry(TypedDict):
    type: Literal["Point"]
    coordinates: list[float]


class FeatureProperties(TypedDict):
    # note: excludes many unused properties
    mag: float
    time: int
    type: Literal["earthquake"]
    place: str
    updated: int
    url: str
    detail: str
    code: str


class EarthquakeFeature(TypedDict):
    geometry: FeatureGeometry
    properties: FeatureProperties
    id: str
    type: Literal["Feature"]


class EarthquakeFetchData(TypedDict):
    bbox: list[float]
    features: list[EarthquakeFeature]
