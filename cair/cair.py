import math
import numpy as np
from typing import Any, Optional
from PIL.Image import Image
from cair_types import Coordinate, LoadImage, ImageSize, SingleImage


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
        energy_map_image = self.__calculate_energy_map(
            image=self.pixel_values,
            image_size=self.image_size,
        )

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

        return int(math.sqrt(left_energy + right_energy))

    def __get_pixel(
        self,
        image: SingleImage,
        coordinate: Coordinate,
    ) -> list[int]:
        """
        Gets the pixel values at a specific coordinate
        """

        # Issue indexing into image
        assert (
            coordinate.x >= 0
        ), f"coordinate.x should be more than 0 but was : {coordinate.x}"
        assert coordinate.y < len(
            image
        ), f"coordinate.y should be less than {len(image)} but was {coordinate.y}"
        assert coordinate.x < len(
            image[0]
        ), f"coordinate.x should be less than {len(image[0])} but was {coordinate.x}"
        pixel = image[coordinate.y][coordinate.x]
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

    def __matrix(
        self,
        width: int,
        height: int,
        fill_with: Any,
    ) -> list[list[Any]]:
        """
        Creates a matrix of width and height with a filler value inside it
        """
        matrix = np.full((height, width), fill_value=fill_with).tolist()
        assert (
            len(matrix) == height
        ), f"matrix should have {height} rows but has {len(matrix)}"
        assert (
            len(matrix[0]) == width
        ), f"matrix should have {width} columns but has {len(matrix[0])}"
        return matrix

    def __calculate_energy_map(
        self,
        image: SingleImage,
        image_size: ImageSize,
    ):
        energy_map = self.__matrix(
            width=len(image[0]),
            height=len(image),
            fill_with=None,
        )
        assert len(energy_map) == len(
            image
        ), f"energy map should have {len(image)} rows but has {len(energy_map)} rows"
        assert len(energy_map[0]) == len(
            image[0]
        ), f"energy map should have {len(image[0])} columns but has {len(energy_map[0])} columns"
        for y in range(len(image) - 1):
            for x in range(len(image[0]) - 1):
                left = (
                    self.__get_pixel(
                        image=image,
                        coordinate=Coordinate(x=x - 1, y=y),
                    )
                    if (x - 1) >= 0
                    else None
                )
                middle = self.__get_pixel(
                    image=image,
                    coordinate=Coordinate(
                        x=x,
                        y=y,
                    ),
                )
                right = (
                    self.__get_pixel(
                        image=image,
                        coordinate=Coordinate(x=x + 1, y=y),
                    )
                    # Not sure if this is correct
                    if (x + 1) <= len(image[0]) - 1
                    else None
                )
                # Issue with indexing
                pixel_energy = self.__get_pixel_energy(
                    left=left,
                    middle=middle,
                    right=right,
                )
                energy_map[y][x] = pixel_energy
        return energy_map


if __name__ == "__main__":
    path = "./cair/best-hot-air-balloon-rides-cappadocia-turkey.jpg"
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
