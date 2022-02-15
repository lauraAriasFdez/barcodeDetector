"""
1. Images for training and validation were downloaded using the OIDV4_toolkit
2. Convert labels to yolov4 format thanks to conver_annotatio.py from https://github.com/theAIGuysCode/OIDv4_ToolKit
3. Create test.txt train.txt with the directories needed for training - I created get_img.py
4. Put the datasets of training and testing in a zip file in my google drive
"""

import os
from stat import filemode


image_files = []
train_path = os.path.join(os.path.join(os.getcwd(),"train"),"obj")
test_path = os.path.join(os.path.join(os.getcwd(),"validation"),"test")

## TEST FILES
for filename in os.listdir(test_path):
    if filename.endswith(".jpg"):
        image_files.append("data/test/" + filename)

with open("test.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()

### TRAIN FILES
image_files = []

for filename in os.listdir(train_path):
    if filename.endswith(".jpg"):
        image_files.append("data/obj/" + filename)

with open("train.txt", "w") as outfile:
    for image in image_files:
        outfile.write(image)
        outfile.write("\n")
    outfile.close()