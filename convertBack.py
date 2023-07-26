import re
import os
from PIL import Image
import glob
import json
import cv2

numbers = re.compile(r'(\d+)')


def bitsToBytes(a):
    s = i = 0
    for x in a:
        s += s + x
        i += 1
        if i == 8:
            yield s
            s = i = 0
    if i > 0:
        yield s << (8 - i)


def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts


def readImagesData(imagesDir="Images/", makeInBlocks=False):
        bytes_ = []
        os.chdir(imagesDir)
        fileMetaData = []
        metaDataApproaching = False
        for imageName in sorted(glob.glob('*.png'), key=numericalSort):
            print(imageName)
            image = Image.open(imageName)
            pixels = image.load()
            width, height = image.size
            for x in range(0, width, 1+makeInBlocks):
                for y in range(0, height, 1+makeInBlocks):
                    if makeInBlocks:
                        total = (sum(pixels[x, y]+pixels[x, y+1]+pixels[x+1, y]+pixels[x+1, y+1])/12)
                        final = 0 if total < 10 else 1
                        bytes_.append(final)

                        continue

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

        if makeInBlocks:
            bytes_ = bitsToBytes(bytes_)
            with open("../output.file", "wb") as file:
                file.write(bytes(bytes_))
        else:
            json_ = bytes(fileMetaData[3:])
            json_ = json.loads(json_.decode())
            print(json_['fileName'])
            with open(f"../output_{json_['fileName']}", 'wb')  as file:
                file.write(bytes(bytes_))

def filify(videoDir="Images/cvout.avi", imagesDir="Images/", makeInBlocks=False):
    cap = cv2.VideoCapture(videoDir)

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
        image_path = f"{imagesDir}image{i:04d}.png"
        cv2.imwrite(image_path, frame)

    # Release the video capture object
    cap.release()
    readImagesData(makeInBlocks=makeInBlocks)