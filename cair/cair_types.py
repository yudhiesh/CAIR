from pprint import pprint
from PIL import Image
from typing import NamedTuple, Optional, TypedDict
from dataclasses import dataclass


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


class Color(NamedTuple):
    """NamedTuple of the color values(RGBA)"""

    red: int
    green: int
    blue: int
    alpha: int


# A single image contains a sequence of Color
SingleImage = list[Color]


@dataclass
class ImageOriginal:
    """
    Class that reads in the image and then outputs the image and the pixel
    values
    """

    img_path: str
    to_width: int

    def __post_init__(self):
        self.img, self.pixel_values = self.run()

    def run(self) -> Optional[tuple[Image.Image, SingleImage]]:
        try:
            img = Image.open(self.img_path)
            image_values = list(img.getdata())
            pixel_values = [
                Color(
                    red=pixel[0],
                    green=pixel[1],
                    blue=pixel[2],
                    alpha=pixel[3],
                )
                for pixel in image_values
            ]
            return img, pixel_values
        except IOError as e:
            print(f"Error when loading image: {e!r}")


@dataclass
class ImageProcessed:
    """Class of the processed images"""

    img: SingleImage
    size: ImageSize


if __name__ == "__main__":
    path = "../../Desktop/SMREITERATE2.png"
    io = ImageOriginal(img_path=path, to_width=500)
    img = io.img
    pixel_values = io.pixel_values
    pprint(pixel_values)
