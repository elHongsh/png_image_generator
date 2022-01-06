# PNG Image Generator

PNG image generator is a true color with alpha image generator!

## Features

It has very simple feature. Generate True color type of PNG file!


## Sample

Samples below are 256x256 image, but it does not mean that implementation cannot support other width or height of image.

### The Entropy (spread RGB randomly)
![TheEntropy](https://user-images.githubusercontent.com/51532228/148304799-58340a41-d0c1-443e-9e64-a4a1ec56996c.png)  
Image size: 256x256
```python
# The Entropy
from random import Random
from typing import List

from png.generator import TrueColorImageGenerator
from png.image import Color


def random_line(length: int) -> List[Color]:
    r = Random()
    return [Color(r.randint(0, 255), r.randint(0, 255), r.randint(0, 255)) for _ in range(0, length)]


if __name__ == '__main__':
    image_array = [random_line(256) for _ in range(0, 256)]
    image = TrueColorImageGenerator.create_image_from_array(image_array)

    with open(f'image_{image.width}x{image.height}1.png', 'wb') as f:
        f.write(image.data)
```

### Red Gradation (0~255, 0, 0, 255)
![RedGradation](https://user-images.githubusercontent.com/51532228/148305164-8abeb01f-d240-4faa-9015-59399f1ddaa1.png)  
Image size: 256x256
```python
# Red Gradation
from png.generator import TrueColorImageGenerator
from png.image import Color

if __name__ == '__main__':
    image_array = [[Color(x, 0, 0, 255) for x in range(0, 255)] for y in range(0, 255)]
    image = TrueColorImageGenerator.create_image_from_array(image_array)

    with open(f'image_{image.width}x{image.height}.png', 'wb') as f:
        f.write(image.data)
```


## PNG Structure

|   Element    | Data size (byte) |
|:------------:|:----------------:|
| Signature    |        8         |
|    Length    |        4         |
|  Chunk Type  |        4         |
|  Chunk Data  |     var > 0      |
|     CRC      |        4         |


### Signature

Signature is a value that all PNG have to start with 0x89504E470D0A1A0A (Big endian).  
Each byte has a different meaning. see the below.

| Hex Value(s) | Purpose                                                                                                 |
|:------------:|---------------------------------------------------------------------------------------------------------|
|      89      | It is a value to reduce the chance that a text file is mistakenly interpreted as a PNG, or vice versa.  |
|   50 4E 47   | It is a letters 'PNG' in ASCII that allowing a person to identify the format easily.                    |
|    0D 0A     | A DOS-sytle line ending to detect DOS-Unix line ending conversion of the data.                          |
|      1A      | A byte that stops display of the file under DOS when the command type has been used.                    |
|      0A      | A Unix-style line ending to detect Unix-DOS line ending conversion.                                     |

### Chunks within the file

#### Chunk Type

PNG header must have three types that is IHDR, IDAT and IEND.  

* IHDR  
  (Must be the first chunk)  
  It contains the image metadata.  

|        Type         | Value or Size                                       | 
|:-------------------:|-----------------------------------------------------| 
|        Width        | 4 bytes                                             | 
|       Height        | 4 bytes                                             | 
|      Bit depth      | 1 byte one of value in 1, 2, 4, 8 or 16             | 
|     Color type      | 1 byte, one of value in 0, 2, 3, 4 or 6             | 
| Compression method  | 1byte, value 0                                      | 
|    Filter method    | 1 byte, value 0                                     | 
|  Interlace method   | 1 byte, value 0(no interlace) or 1(Adam7 interlace) |

This project currently do not support customization except width and height.  
<pre>
- Default bit depth is 8.
- Color type always set 6.
- Compression method always set 0.
- Filter method always set 0; adaptive filtering.  
- Interlace method always set 0; no interlace.
</pre>

* PLTE  
It contains the palette.  
* IDAT  
It contains the actual image data, which is the output stream of the compression algorithm.  
* IEND  
(Must be stored in end of the chunk)  
It marks the image end.

#### Chunk Data

In our implementation, we only support true color with alpha image, so all chunk data contains R, G, B and A.

#### CRC

Every chunk has its own 4 bytes of CRC.  It is always appended to end of the chunk.  

[Reference: Portable Network Graphics(PNG) from Wikipedia](https://en.wikipedia.org/wiki/Portable_Network_Graphics)