
# Run the file that detects the barcode 
import subprocess
import shutil

import cv2
import time
from cv2 import imshow
from cv2 import waitKey 
results_path = "../yolov5-master/runs/detect/barcode/labels/results.txt"
timeout_video = 60

from os.path import exists


def barcode_obj_detect(path):
    
    if (exists("../yolov5-master/runs/detect/barcode")):
        shutil.rmtree("../yolov5-master/runs/detect/barcode")

    subprocess.run(['python3', '../yolov5-master/detect.py',"--weights", "barcode_model.pt", "--source" ,path,"--name","barcode","--save-txt"])

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
    capture.set(3,640)#width
    capture.set(4,480)#height

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
                    #every 30 second run obj detector to check if barcode is present and can could not be scannerd
                    #check barcode if exists cut it and pass it to check barcodes
                    cv2.imwrite("../yolov5-master/runs/detect//img.jpg", img)  # 480 by 640
                    res = barcode_obj_detect("../yolov5-master/runs/detect//img.jpg")

                    if res !=[]:
                        center_x,center_y,w,h = res
                        x,y,_ = img.shape
                        
                        width = int (x * w)
                        height = int (h*y)
                        cent_x = int(center_x*x) 
                        cent_y = int(center_y*y) 
                        x_Start = cent_x - width//2
                        y_Start = cent_y - height//2

                        cropped_image = img[x_Start:, y_Start:]
                        imshow("img",cropped_image)
                        waitKey(0)

                
        else:
            print ("camera could not read image")
            break

        ## adds a delay and escapes a video  - used only for debuggin
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


#barcode_obj_detect("./melinda.jpg")
video_capture()