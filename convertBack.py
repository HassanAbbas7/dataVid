import re
import os
from PIL import Image
import glob
import json
import cv2

numbers = re.compile(r'(\d+)')


def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts


def readImagesData(imagesDir="Images/"):
        bytes_ = []
        os.chdir(imagesDir)
        fileMetaData = []
        metaDataApproaching = False
        for imageName in sorted(glob.glob('*.png'), key=numericalSort):
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
        json_ = bytes(fileMetaData[3:])
        json_ = json.loads(json_.decode())
        print(json_['fileName'])
        with open(f"../output_{json_['fileName']}", 'wb')  as file:
            file.write(bytes(bytes_))

def filify(videoDir="Images/cvout.avi", imagesDir="Images/"):
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
    readImagesData()