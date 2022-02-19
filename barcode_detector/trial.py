
# Run the file that detects the barcode 
import subprocess
import cv2
import os
import shutil
results_path = ".../yolov5-master/runs/detect/barcode/labels/results.txt"

def barcode_obj_detect(path):
    subprocess.run(['python3', '../yolov5-master/detect.py',"--weights", "barcode_model.pt", "--source" ,path,"--name","barcode","--save-txt"])

    f = open(results_path, "r")
    # get txt value
    for line in f:
        if line[0] =="1":
            print("barcode detected")
        print(line)
    f.close()
    # delete folder 
    shutil.rmtree("../yolov5-master/runs/detect/barcode")



barcode_obj_detect("./melinda.jpg")