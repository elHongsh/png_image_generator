class TrueColorImage:
    width: int
    height: int
    data: bytes

    def __init__(self, width: int, height: int, data: bytes):
        self.width = width
        self.height = height
        self.data = data


class Color:
    r: int = 0
    g: int = 0
    b: int = 0
    a: int = 255

    def __init__(self, r: int, g: int, b: int, a: int = 255):
        if 0 <= r <= 255:
            self.r = r
        if 0 <= g <= 255:
            self.g = g
        if 0 <= b <= 255:
            self.b = b
        if 0 == a or 255 == a:
            self.a = a


class ColorFactory:
    TRANSPARENT = Color(0, 0, 0, 0)
    BLACK = Color(0, 0, 0, 255)
    DARK_RED = Color(128, 0, 0, 255)
    RED = Color(255, 0, 0)
    PINK = Color(255, 0, 255)
    TEAL = Color(0, 128, 128)
    GREEN = Color(0, 128, 0)
    LIGHT_GREEN = Color(0, 255, 0)
    TURQUOISE = Color(0, 255, 255)
    DARK_BLUE = Color(0, 0, 128)
    VIOLET = Color(128, 0, 128)
    BLUE = Color(0, 0, 255)
    LIGHT_GRAY = Color(192, 192, 192)
    GARY = Color(128, 128, 128)
    DARK_YELLOW = Color(128, 128, 0)
    YELLOW = Color(255, 255, 0)
    WHITE = Color(255, 255, 255, 255)
    ORANGE = Color(0xFF, 0x85, 0x1B, 255)

