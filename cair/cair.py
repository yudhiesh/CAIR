from typing import TypedDict


class ImageSize(TypedDict):
    """Dictionary of the image size which contains the width and height"""

    width: int
    height: int


class Coordinate(TypedDict):
    """The coordinates of the pixels"""

    x: int
    y: int


# The seam is a sequence of pixels
Seam = list[Coordinate]

# Energy Map is a 2D list that has the same width and height as the image the
# map is being calculated for
EnergyMap = list[list[int]]


class Color(TypedDict):
    """Dictionary of the color values(RGBA)"""

    red: int
    green: int
    blue: int
    alpha: int
