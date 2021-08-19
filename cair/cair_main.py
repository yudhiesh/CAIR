import math
from typing import Any, Optional
from PIL.Image import Image
from cair.cair_types import Coordinate, LoadImage, ImageSize, SingleImage


class ResizeImageWidth:
    def __init__(
        self,
        img: Image,
        pixel_values: SingleImage,
        image_size: ImageSize,
        resize_to: int,
    ) -> None:
        self.img: Image = img
        self.pixel_values: SingleImage = pixel_values
        self.image_size: ImageSize = image_size
        self.resize_to = resize_to
        self.run()

    def run(self):
        ...

    def __pixels_to_remove(self) -> int:
        """
        Finds the number of pixels to remove to achieve the desired resized
        image size(only works for width right now)
        """
        pixels = self.image_size.width - self.resize_to
        if pixels <= 0:
            error_message = (
                f"Please pass a smaller value to resize_to than {self.image_size.width}"
            )
            raise ValueError(error_message)
        return pixels

    def __get_pixel_energy(
        self,
        left: Optional[list[int]],
        middle: list[int],
        right: Optional[list[int]],
    ) -> float:
        """
        Gets the pixel energy of the middle pixel based on the pixels on the left
        and on the right
        """
        middle_red, middle_green, middle_blue, middle_alpha = middle
        left_energy, right_energy = 0, 0
        if left:
            left_red, left_green, left_blue, left_alpha = left
            left_energy = (
                ((left_red - middle_red) ** 2)
                + ((left_green - middle_green) ** 2)
                + ((left_blue - middle_blue) ** 2)
                + ((left_alpha - middle_alpha) ** 2)
            )
        if right:
            right_red, right_green, right_blue, right_alpha = right
            right_energy = (
                ((right_red - middle_red) ** 2)
                + ((right_green - middle_green) ** 2)
                + ((right_blue - middle_blue) ** 2)
                + ((right_alpha - right_alpha) ** 2)
            )

        return math.sqrt(left_energy + right_energy)

    def __get_pixel(
        self,
        image: SingleImage,
        coordinate: Coordinate,
    ) -> list[int]:
        """
        Gets the pixel values at a specific coordinate
        """
        pixel = image[coordinate.x][coordinate.y]
        return pixel

    def __set_pixel(
        self,
        image: SingleImage,
        coordinate: Coordinate,
        color: list[int],
    ) -> None:
        """
        Sets a specific coordinate value in an image to a list of values
        """
        image[coordinate.x][coordinate.y] = color

    def __matrix(self, width: int, height: int, fill_with: Any) -> list[list[Any]]:
        """
        Creates a matrix of width and height with a filler value inside it
        """
        matrix = [[fill_with for _ in range(height + 1)] for _ in range(width + 1)]
        return matrix


if __name__ == "__main__":
    path = "/Users/yravindranath/cair/cair/best-hot-air-balloon-rides-cappadocia-turkey.jpg"
    io = LoadImage(img_path=path)
    img = io.img
    pixel_values = io.pixel_values
    image_size = io.image_size
    ResizeImageWidth(
        img=img,
        pixel_values=pixel_values,
        image_size=image_size,
        resize_to=500,
    )
