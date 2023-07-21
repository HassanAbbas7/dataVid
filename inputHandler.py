from PIL import Image
import numpy as np
from itertools import zip_longest
import glob
import re
from numba import jit, cuda
import os
from time import sleep
import cv2


class vidizer():
    def __init__(self):
        self.numbers = re.compile(r'(\d+)')
        self.imageSize = (300, 300)
        pass
    
    def convertIntoBytes(self, filePath):
        with open(filePath, "rb") as file:
            return list(file.read())
        
    
    def getBlankImage(self, imageSize):
        image = Image.new("RGB", imageSize, "white")
        return image


    def writeDataToImage(self, data, image, no):
        print(len(data))
        bytes_ = np.array(data).reshape(image.size)
        pixels = image.load()
        width, height = image.size
        for x in range(width):
            for y in range(height):
                if bytes_[x,y] == (256):
                    pixels[x, y] = (0, 0, 255)
                else:
                    pixels[x, y] = (bytes_[x,y], 0, 0)
        image.save(f"Images/image{no}.png")
        
    def sliceData(self, data, sets, fillvalue):
        for group in zip_longest(*[iter(data)] * sets, fillvalue=fillvalue):
            yield list(group)
            
    def numericalSort(self, value):
        parts = self.numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts


    def makeVideoCv(self):
        fps = 10
        video_name = "cvout"
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        img_array = []
        for fileName in sorted(glob.glob('Images/*.png'), key=self.numericalSort):
            print("hello")
            img = cv2.imread(fileName)
            height, width, layers = img.shape
            size = (width, height)
            print(size)
            img_array.append(img)

        out = cv2.VideoWriter(f"Images/{video_name}.avi", fourcc, fps, size)

        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
    
    def makeVideo(self):
        os.chdir("Images/")
        os.system("ffmpeg -i image%d.png -r 5 -c:v mjpeg -qscale:v 0 test.avi")
        # os.system("del *.png")


    def makeImages(self, fileName):
        x = 0
        bytes_ = self.convertIntoBytes(fileName)
        for _ in self.sliceData(bytes_, (self.imageSize[0]*self.imageSize[0]), 256):
            x = x + 1
            self.writeDataToImage(_, self.getBlankImage(self.imageSize), x)
        self.makeVideoCv()


    def convertBack(self):
        bytes_ = []
        numbers = re.compile(r'(\d+)')
        os.chdir("Images/")
        # os.system('ffmpeg -i output.mp4 -vf "fps=2" image%d.png')
        # sleep(2)
        # os.system("dir")
        # sleep(1)
        for imageName in sorted(glob.glob('*.png'), key=self.numericalSort):
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
        f = open("out.exe", 'wb') 
        f.write(bytes(bytes_))
        f.close()

    

vidizer = vidizer()
vidizer.makeVideoCv()
