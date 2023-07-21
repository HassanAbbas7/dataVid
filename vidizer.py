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

class vidizer():
    def __init__(self):
        self.numbers = re.compile(r'(\d+)')
        self.imageSize = (300, 300)
        self.fileData = {"fileName": "", "fileSize": None}
        pass
    
    def convertIntoBytes(self, filePath):
        with open(filePath, "rb") as file:
            return list(file.read())
        
    
    def getBlankImage(self, imageSize):
        image = Image.new("RGB", imageSize, "white")
        return image


    def writeDataToImage(self, data, image, no):
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
    

    def bytes_to_bit_string(self, byte_data):
        bit_string = ''.join(format(byte, '08b') for byte in byte_data)
        return bit_string


    def bit_string_to_bytes(self, bit_string):
        # Ensure the bit string length is a multiple of 8 (8 bits per byte)
        padded_bit_string = bit_string.zfill((len(bit_string) + 7) // 8 * 8)

        # Convert the padded bit string to bytes
        byte_data = bytes(int(padded_bit_string[i:i+8], 2) for i in range(0, len(padded_bit_string), 8))

        return byte_data

    def vidize(self, fileName):
        x = 0
        fileSize = os.path.getsize(fileName)
        self.fileData = {"fileName": fileName, "fileSize": fileSize}
        fileDataBytes = list(bytes(json.dumps(self.fileData), encoding='utf-8'))
        print(fileDataBytes)
        input()
        bytes_ = self.convertIntoBytes(fileName)
        bytes_.extend([257, 257, 257] + fileDataBytes)
        for _ in self.sliceData(bytes_to_bit_string(bytes_), (self.imageSize[0]*self.imageSize[0])/4, 256):
            x = x + 1
            # self.writeDataToImage(_, self.getBlankImage(self.imageSize), x)
            self.experimentalWriteToImage(_, self.getBlankImage(self.imageSize), x)
        self.makeVideoCv()



    def experimentalWriteToImage(self, data, image, no):
        bits = self.bytes_to_bit_string(list(bytes("This is a test string..."*no, encoding='utf-8')))
        bytes_ = (self.bit_string_to_bytes(bits))
        print(bytes_)
        input()

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
        fileMetaData = []
        metaDataApproaching = False
        for imageName in sorted(glob.glob('*.png'), key=self.numericalSort):
            print(imageName)
            image = Image.open(imageName)
            pixels = image.load()
            width, height = image.size
            for x in range(width):
                for y in range(height):
                    if pixels[x,y][0] >= 0:
                        if pixels[x, y][2] == 255:
                            metaDataApproaching = False
                            continue
                        if pixels[x,y][1] == 200:
                            print("getting meta data indicator")
                            metaDataApproaching = True
                            
                        if metaDataApproaching:
                            fileMetaData.append(pixels[x,y][0])
                        else:
                            bytes_.append(pixels[x,y][0])
                            
            os.remove(imageName)

        print(len(fileMetaData))
        json_ = bytes(fileMetaData[3:])
        json_ = json.loads(json_.decode())
        print(json_['fileName'])
        with open(f"../output_{json_['fileName']}", 'wb')  as file:
            file.write(bytes(bytes_))




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
