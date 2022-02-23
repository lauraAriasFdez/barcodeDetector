
# Run the file that detects the barcode 
import re
import subprocess
import shutil

import cv2
import time
from cv2 import imshow
from cv2 import waitKey
from prettytable import NONE 
results_path = "../yolov5-master/runs/detect/barcode/labels/results.txt"
timeout_video = 60

from os.path import exists


def barcode_obj_detect(path):
    
    if (exists("../yolov5-master/runs/detect/barcode")):
        shutil.rmtree("../yolov5-master/runs/detect/barcode")

    subprocess.run(['python3', '../yolov5-master/detect.py',"--weights", "barcode_model.pt", "--source" ,path,"--name","barcode","--save-txt"])

    result = None
    if (exists(results_path)):
        f = open(results_path, "r")
        # get txt value
        for line in f:
            if line[0] =="1":
                print("barcode detected")
                result = line.split(" ")
                result = result[1: ]
                for i in range(len(result)):
                    result[i] = float(result[i])
        f.close()
        
    return result # [center_x, center_y, w,h]


## BARCODE DETECTION WITH OPEN CV
import pyzbar.pyzbar as zbar
def check_barcode(img):
    return zbar.decode(img)
               
def video_capture():
    #get the camera
    capture = cv2.VideoCapture(0)

    #size of the screen shown 
    capture.set(3,416)#width
    capture.set(3,416)#height

    ## start time out for camera
    startTime =  time.time()

    #Video Capture
    while True:
        success,img = capture.read()

        ## TIME LIMIT TO FIND BARCODE
        timeElapsed = int (time.time() - startTime)
        if (timeElapsed > timeout_video):
            return -1

        # If image capture correctly 
        if success:
            cv2.imshow("Frame",img)
            barcodes = check_barcode(img)
            if barcodes != []:
                return barcodes
            else:
                if (timeElapsed%30==0):
                    #every 30 second run obj detector to check if barcode is present 
                    #check barcode if exists cut it and pass it to check barcodes
                    #resize img
                    resized = cv2.resize(img,(416,416),interpolation=cv2.INTER_AREA)
                    cv2.imwrite("../yolov5-master/runs/detect/img.jpg", resized) 
                    res = barcode_obj_detect("../yolov5-master/runs/detect/img.jpg")

                    if res !=None:
                        xcenter, ycenter, b_width,b_height  = res

                        width,height,_ = resized.shape
                        center_x = int (width* xcenter)
                        center_y = int(height *ycenter)
                        print ("the center is ",center_x," ", center_y)
                        print ("the shap is ",img.shape)

                        obj_height  = int(height * b_height)
                        obj_width = int(width * b_width)

                        ymin = center_y - obj_height
                        xmin = center_x - obj_width
                        xmax = center_x + obj_width
                        ymax = center_y + obj_height

                        cv2.rectangle(resized, (xmin, ymin), (xmax, ymax), (0, 255, 0))
                        imshow("img",resized)
                        waitKey(0)

                
        else:
            print ("camera could not read image")
            break

        ## adds a delay and escapes a video  - used only for debuggin
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


#barcode_obj_detect("./melinda.jpg")
video_capture()