from PIL.Image import Image
from cair.cair_types import LoadImage, ImageSize, SingleImage


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
        if self.image_size.width < self.resize_to:
            error_message = (
                f"Resize to is bigger than the actual image width\n"
                f"Please pass a value smaller than {self.image_size.width}"
            )
            raise ValueError(error_message)


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
