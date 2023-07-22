import cv2
from PIL import Image
from itertools import zip_longest
import numpy as np
import json
import os
import glob
import re

numbers = re.compile(r'(\d+)')

def bytes_to_bit_string(byte_data):
    bit_string = ''.join(format(byte, '08b') for byte in byte_data)
    return bit_string


def convertIntoBytes(filePath):
        with open(filePath, "rb") as file:
            return list(file.read())


def getBlankImage(imageSize):
    image = Image.new("RGB", imageSize, "white")
    return image



def writeDataToImage(data, image, no):
    bytes_ = np.array(data).reshape(image.size)
    pixels = image.load()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            if bytes_[x,y] == (256):
                pixels[x, y] = (0, 0, 255)
            elif bytes_[x,y] == (257):
                print("printing meta data indicator 257")
                pixels[x, y] = (0, 200, 0)
            else:
                pixels[x, y] = (bytes_[x,y], 0, 0)
    image.save(f"Images/image{no}.png")



def sliceData(data, sets, fillvalue):
    for group in zip_longest(*[iter(list(data))] * int(sets), fillvalue=fillvalue):
        yield list(group)


def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def makeVideoCv():
    fps = 10
    video_name = "cvout"
    fourcc = cv2.VideoWriter_fourcc('R','G','B','A')
    img_array = []
    for fileName in sorted(glob.glob('Images/*.png'), key=numericalSort):
        print("hello")
        img = cv2.imread(fileName)
        height, width, layers = img.shape
        size = (width, height)
        print(size)
        img_array.append(img)
        os.remove(fileName)

    out = cv2.VideoWriter(f"Images/{video_name}.avi", fourcc, fps, size)

    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()



def vidize(fileName, makeInBlocks=False, blockSize=4, imageSize=(300, 300)):
    x = 0
    fileSize = os.path.getsize(fileName)
    fileData = {"fileName": fileName, "fileSize": fileSize}
    fileDataBytes = list(bytes(json.dumps(fileData), encoding='utf-8'))
    print(fileDataBytes)
    input()
    bytes_ = convertIntoBytes(fileName)
    bytes_.extend([257, 257, 257] + fileDataBytes)

    if makeInBlocks:
        data = bytes_to_bit_string(bytes_)
    else:
        data = bytes_


    for _ in sliceData(data, (imageSize[0]*imageSize[0])/(blockSize if makeInBlocks else 1), 256):
        x = x + 1
        writeDataToImage(_, getBlankImage(imageSize), x)
    makeVideoCv()