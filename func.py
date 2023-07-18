from PIL import Image
import numpy as np
from itertools import zip_longest
import glob
import re
from numba import cuda


numbers = re.compile(r'(\d+)')
def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts


# @vectorize(['float32(float32)'], target='cuda')
@cuda.jit
def readImages(outputName):
    bytes_ = []
    numbers = re.compile(r'(\d+)')
    for imageName in sorted(glob.glob('**/*.png'), key= numericalSort):
        print(imageName)
        image = Image.open(imageName)
        pixels = image.load()
        width, height = image.size
        for x in range(width):
            for y in range(height):
                if pixels[x,y][0] >= 0:
                    if pixels[x,y][2] == 255:
                        continue
                    bytes_.append(pixels[x,y][0])
#         print(len(bytes_))
    f = open(outputName, 'wb') 
    f.write(bytes(bytes_))
    f.close()
    return bytes_


readImages()