import numpy as np
from PIL import Image
from typing import NamedTuple, Optional
from dataclasses import dataclass


@dataclass
class ImageSize:
    """Image size which contains the width and height"""

    width: int
    height: int


@dataclass
class Coordinate:
    """The coordinates of the pixels"""

    x: int
    y: int


# The seam is a sequence of pixels
Seam = list[Coordinate]

# Energy Map is a 2D list that has the same width and height as the image the
# map is being calculated for
EnergyMap = list[list[int]]


class Color(NamedTuple):
    red: int
    green: int
    blue: int
    alpha: int


# A single image contains a 3D list of ints
SingleImage = list[list[list[Color]]]


@dataclass
class LoadImage:
    """
    Class that reads in the image and then outputs the image and the pixel
    values
    """

    img_path: str

    def __post_init__(self):
        self.img, self.pixel_values, self.image_size = self.run()  # type: ignore

    def run(self) -> Optional[tuple[Image.Image, SingleImage, ImageSize]]:
        try:
            # Convert the image to a RGBA image as it might be RGB
            img = Image.open(self.img_path).convert("RGBA")
            width, height = img.size
            channels = len(img.getbands())
            image_size = ImageSize(height=height, width=width)
            print(f"Image shape: ({width},{height},{channels})")
            # Convert 1D image to 3D image
            pixel_values = (
                np.asarray(list(img.getdata()))
                .reshape(
                    (width, height, -1),
                )
                .tolist()
            )
            return img, pixel_values, image_size  # type: ignore
        except IOError as e:
            print(f"Error when loading image: {e!r}")


@dataclass
class ImageProcessed:
    """Class of the processed images"""

    img: SingleImage
    size: ImageSize
