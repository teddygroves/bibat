"""Provides the base class PreparedData."""

from pydantic import BaseModel, ConfigDict

from bibat.util import CoordDict


class PreparedData(BaseModel):
    """What prepared data looks like in a bibat analysis."""

    name: str
    coords: CoordDict
    model_config = ConfigDict(arbitrary_types_allowed=True)
