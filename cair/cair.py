from cair_types import ImageOriginal


if __name__ == "__main__":
    path = "/Users/yravindranath/cair/cair/best-hot-air-balloon-rides-cappadocia-turkey.jpg"
    io = ImageOriginal(img_path=path, to_width=500)
    img = io.img
    pixel_values = io.pixel_values
    image_size = io.image_size
    img.show()
