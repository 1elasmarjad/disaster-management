from typing import Literal, TypedDict

from proj_types.earthquake_api import FeatureGeometry


class Disaster(TypedDict):
    type: Literal["earthquake"]
    geometry: FeatureGeometry

    metadata: dict
