from typing import Literal, TypedDict

from proj_types.thirdparty_api import FeatureGeometry


class Disaster(TypedDict):
    type: Literal["earthquake", "wildfire"]
    geometry: FeatureGeometry

    metadata: dict
