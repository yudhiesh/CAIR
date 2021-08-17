from PIL import Image
from typing import Optional
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


@dataclass
class Color:
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
        self.img, self.pixel_values, self.image_size = self.run()  # type: ignore

    def run(self) -> Optional[tuple[Image.Image, SingleImage, ImageSize]]:
        try:
            # Convert the image to a RGBA image as it might be RGB
            img = Image.open(self.img_path).convert("RGBA")
            width, height = img.size
            channels = len(img.getbands())
            image_size = ImageSize(height=height, width=width)
            print(f"Image shape: ({width},{height},{channels})")
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
            return img, pixel_values, image_size
        except IOError as e:
            print(f"Error when loading image: {e!r}")


@dataclass
class ImageProcessed:
    """Class of the processed images"""

    img: SingleImage
    size: ImageSize
