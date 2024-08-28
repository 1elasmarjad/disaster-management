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


class NASAEVentCategory(TypedDict):
    id: int
    title: str


class NASAGeometry(TypedDict):
    date: str
    type: str
    coordinates: list[float]


class NASAEvent(TypedDict):
    id: str
    title: str
    description: str
    link: str
    categories: list[NASAEVentCategory]
    geometries: list[NASAGeometry]


class NASAEventsFetchData(TypedDict):
    title: str
    description: str
    link: str
    events: list[NASAEvent]
