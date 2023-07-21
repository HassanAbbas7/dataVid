from PIL import Image
import numpy as np
from itertools import zip_longest
import glob
import re
from numba import jit, cuda
import os
from time import sleep
import cv2
import argparse
import json




def bytes_to_bit_string(byte_data):
        bit_string = ''.join(format(byte, '08b') for byte in byte_data)
        return bit_string


def bit_string_to_bytes(bit_string):
    # Ensure the bit string length is a multiple of 8 (8 bits per byte)
    padded_bit_string = bit_string.zfill((len(bit_string) + 7) // 8 * 8)

    # Convert the padded bit string to bytes
    byte_data = bytes(int(padded_bit_string[i:i+8], 2) for i in range(0, len(padded_bit_string), 8))

    return byte_data


def writeDataToImage(data, image, no):
        blockSize = 4

        if data%blockSize != 0:
            raise Exception(f"DataShapeError:{len(data)} could not be divisible by {blockSize}")
            return


        bits = np.array(data).reshape(image.size)

        for i in range(0, matrix_length, block_size):
        for j in range(0, matrix_length, block_size):
            block_data = matrix[i:i+block_size, j:j+block_size]
            block_data = block_data.flatten()  # Flatten the 2D block into a 1D array

            # Ensure the block size is exactly 4x4 (if not, it's the last block)
            block_data.resize((block_size * block_size,), refcheck=False)

            # Write the data to the corresponding pixels in the image
            for k, pixel_value in enumerate(block_data):
                x = j + (k % block_size)
                y = i + (k // block_size)
                image.putpixel((x, y), min(int(pixel_value), max_value))

        return image