"""Provides the base class PreparedData."""

from pydantic import BaseModel

from bibat.util import CoordDict


class PreparedData(BaseModel):
    """What prepared data looks like in a bibat analysis."""

    name: str
    coords: CoordDict
