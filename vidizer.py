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
        fourcc = cv2.VideoWriter_fourcc('R','G','B','A')
        img_array = []
        for fileName in sorted(glob.glob('Images/*.png'), key=self.numericalSort):
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
    


    def vidize(self, fileName):
        x = 0
        bytes_ = self.convertIntoBytes(fileName)
        for _ in self.sliceData(bytes_, (self.imageSize[0]*self.imageSize[0]), 256):
            x = x + 1
            self.writeDataToImage(_, self.getBlankImage(self.imageSize), x)
        self.makeVideoCv()


    def filify(self):
        cap = cv2.VideoCapture("Images/cvout.avi")

        # Check if the video file was opened successfully
        if not cap.isOpened():
            print("Error opening video file")
            return

        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Loop through each frame and save it as an image
        for i in range(frame_count):
            ret, frame = cap.read()

            # Break the loop if the video has ended
            if not ret:
                break

            # Save the frame as an image in the output folder
            image_path = f"Images/image{i:04d}.png"
            cv2.imwrite(image_path, frame)

        # Release the video capture object
        cap.release()
        self.convertBack()

        
    def convertBack(self):
        bytes_ = []
        numbers = re.compile(r'(\d+)')
        os.chdir("Images/")
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
            os.remove(imageName)
        f = open("../out.exe", 'wb') 
        f.write(bytes(bytes_))
        f.close()
        os.remove("Images/cvout.avi")

    



if __name__ == "__main__":
    vidizer = vidizer()
    parser = argparse.ArgumentParser(description="My script description")
    parser.add_argument("--vidize", type=str, help="Description of argument 1")
    parser.add_argument("--filify", type=bool, default=False, help="Description of argument 2")

    args = parser.parse_args()
    if (args.vidize):
        print(args.vidize)
        vidizer.vidize(args.vidize)
    elif args.filify:
        vidizer.filify()