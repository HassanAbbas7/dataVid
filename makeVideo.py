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



def writeDataToImage(data, image, no, makeInBlocks=False):
    bytes_ = (np.array(data).reshape(image.size)) if not makeInBlocks else data
    pixels = image.load()
    width, height = image.size
    tracker = 0
    for x in range(0, width, 1 + makeInBlocks):
        for y in range(0, height, 1 + makeInBlocks):
            if makeInBlocks:
                pixelData = (255,255,255) if str(bytes_[tracker])=='1' else (0,0,0)
                pixels[x, y] = pixelData
                pixels[x, y+1] = pixelData
                pixels[x+1, y] = pixelData
                pixels[x+1, y+1] = pixelData
                tracker = tracker + 1
            else:
                if bytes_[x,y] == (256):
                    pixels[x, y] = (0, 0, 255)
                elif bytes_[x,y] == (257):
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


def makeVideoCv(videoEncoding=True):
    fps = 30
    video_name = "cvout"
    fourcc = cv2.VideoWriter_fourcc('R','G','B','A') if videoEncoding else 0
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



def vidize(fileName, makeInBlocks=True, blockSize=4, imageSize=(300, 300)):
    x = 0
    fileSize = os.path.getsize(fileName)
    fileData = {"fileName": fileName, "fileSize": fileSize}
    fileDataBytes = list(bytes(json.dumps(fileData), encoding='utf-8'))
    bytes_ = convertIntoBytes(fileName)
    bytes_.extend([257, 257, 257] + fileDataBytes)

    if makeInBlocks:
        data = bytes_to_bit_string(bytes_)
    else:
        data = bytes_


    for _ in sliceData(data, (imageSize[0]*imageSize[0])/(blockSize if makeInBlocks else 1), 256):
        x = x + 1
        writeDataToImage(_, getBlankImage(imageSize), x, makeInBlocks=makeInBlocks)
    makeVideoCv(videoEncoding=not makeInBlocks)