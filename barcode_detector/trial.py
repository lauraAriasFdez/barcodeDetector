
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



def directions_where_to_move(res):
    print("Barcode detected but could not scan PLEASE: ")
    center_x,center_y,b_width,b_height = res #0.52524 0.484375 0.112981 0.0649038

    """
    if center to close to the right (close to 1) bring to the left
    if center to close to the left (close to 0) bring to the right

    if height to small (close to zero) bring closer
    if height to large (close to 1) bring further away 
    """
    if (center_x>0.75):
        print("move object to the LEFT")
    elif (center_x < 0.25):
        print ("move object to the RIGHT")
    
    elif (center_y>0.75):
        print("move object UP")
    elif (center_y < 0.25):
        print("move object DOWN")

    elif(b_height < 0.15):
        print("bring object CLOSER")
    elif (b_height >= 0.40):
        print("bring object FURTHER AWAY")
    

## BARCODE DETECTION WITH OPEN CV
import pyzbar.pyzbar as zbar
def check_barcode(img):
    return zbar.decode(img)
               
def video_capture():
    #get the camera
    capture = cv2.VideoCapture(0)

    #size of the screen shown 
    capture.set(3,480)#width
    capture.set(3,640)#height

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
                print ("BARCODE DETECTED___________________")
                return barcodes
            else:
                if (timeElapsed%10==0):
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
                        obj_height  = int(height * b_height)
                        obj_width = int(width * b_width)

                        ymin = center_y - obj_height
                        xmin = center_x - obj_width
                        xmax = center_x + obj_width
                        ymax = center_y + obj_height

                        cropped_img = resized[ymin:ymax,xmin:xmax]
                        barcodes = check_barcode(cropped_img)
                        if barcodes != []:
                            print ("BARCODE DETECTED___________________")
                            return barcodes

                        else:
                            directions_where_to_move(res)

                
        else:
            print ("camera could not read image")
            break

        ## adds a delay and escapes a video  - used only for debuggin
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


#barcode_obj_detect("./melinda.jpg")
video_capture()