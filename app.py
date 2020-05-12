from png.generator import TrueColorImageGenerator
from png.image import Color, ColorFactory

if __name__ == '__main__':
    image_array = [
        [Color(0, 0, 0, 255), Color(0, 0, 0, 0)],
        [Color(0, 0, 0, 0), Color(255, 255, 255, 255), ColorFactory.ORANGE]
    ]
    image = TrueColorImageGenerator.create_image_from_array(image_array)

    with open(f'image_{image.width}x{image.height}.png', 'wb') as f:
        f.write(image.data)
