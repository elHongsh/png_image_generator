import struct
import zlib
from typing import List

from png.image import TrueColorImage, Color


class TrueColorImageGenerator:
    @staticmethod
    def create_image_from_array(data: List[List[Color]]) -> TrueColorImage:
        image: bytes = TrueColorImageGenerator.__create_signature()

        height, width = TrueColorImageGenerator.__get_image_size(data)

        image += TrueColorImageGenerator.__create_ihdr(height, width)
        image += TrueColorImageGenerator.__create_idat(data, height, width)
        image += TrueColorImageGenerator.__create_iend()
        return TrueColorImage(data=image, width=width, height=height)

    @staticmethod
    def __create_signature() -> bytes:
        signature: bytes = b'\x89' + 'PNG\r\n\x1A\n'.encode('ascii')
        return signature

    @staticmethod
    def __get_image_size(data: List[List[Color]]) -> (int, int):
        height = len(data)
        width = 0
        for row in data:
            if width < len(row):
                width = len(row)
        return height, width

    @staticmethod
    def __create_ihdr(height: int, width: int, bit_depth: int = 8) -> bytes:
        """image header presentate the meta information of image"""
        color_type_as_true_with_alpha = 6
        compression_as_deflate: int = 0
        filter_type_as_adaptive_filtering: int = 0
        no_interlace: int = 0

        image_meta: bytes = TrueColorImageGenerator.__4b_int_be(width)
        image_meta += TrueColorImageGenerator.__4b_int_be(height)
        image_meta += TrueColorImageGenerator.__1b_int_be(bit_depth)
        image_meta += TrueColorImageGenerator.__1b_int_be(color_type_as_true_with_alpha)
        image_meta += TrueColorImageGenerator.__1b_int_be(compression_as_deflate)
        image_meta += TrueColorImageGenerator.__1b_int_be(filter_type_as_adaptive_filtering)
        image_meta += TrueColorImageGenerator.__1b_int_be(no_interlace)

        block = 'IHDR'.encode('ascii') + image_meta
        crc = TrueColorImageGenerator.__4b_int_be(zlib.crc32(block))

        ihdr = TrueColorImageGenerator.__4b_int_be(len(image_meta))
        ihdr += block
        ihdr += crc
        print(ihdr)
        return ihdr

    @staticmethod
    def __create_idat(data: List[List[Color]], height: int, width: int) -> bytes:
        raw_data: bytes = b''
        for y in range(0, height):
            raw_data += b'\0'
            for x in range(0, width):
                c = TrueColorImageGenerator.__4b_int_be(0)  # default color is transparent.
                if y < len(data) and x < len(data[y]):
                    c = TrueColorImageGenerator.__1b_int_be(data[y][x].r)
                    c += TrueColorImageGenerator.__1b_int_be(data[y][x].g)
                    c += TrueColorImageGenerator.__1b_int_be(data[y][x].b)
                    c += TrueColorImageGenerator.__1b_int_be(data[y][x].a)
                raw_data += c

        compressor = zlib.compressobj()
        compressed_data = compressor.compress(raw_data)
        compressed_data += compressor.flush()

        block = 'IDAT'.encode('ascii') + compressed_data
        crc = TrueColorImageGenerator.__4b_int_be(zlib.crc32(block))

        idat = TrueColorImageGenerator.__4b_int_be(len(compressed_data))
        idat += block
        idat += crc
        print(idat)
        return idat

    @staticmethod
    def __create_iend() -> bytes:
        length = TrueColorImageGenerator.__4b_int_be(0)
        chunk_type = 'IEND'.encode('ascii')
        crc = TrueColorImageGenerator.__4b_int_be(zlib.crc32(chunk_type))
        iend = length + chunk_type + crc
        print(iend)
        return iend

    @staticmethod
    def __1b_int_be(value: int) -> bytes:
        return struct.pack('!B', value & (2 ** 8 - 1))

    @staticmethod
    def __4b_int_be(value: int) -> bytes:
        return struct.pack('!I', value & (2 ** 32 - 1))
