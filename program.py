import torch
#import matplotlib.pyplot as plt
import numpy as np
model = torch.hub.load("ultralytics/yolov5","custom",path="yolov5-master/barcode_model.pt")

img = "C:/Users/larfe/OneDrive/Imágenes/melinda.jpg"
results = model(img)
results.print()
results.show()

results.pandas().xyxy[0]

#plt.imshow(np.squeeze(results.render()))
#plt.show()


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
        if success:
            cv2.imshow("Frame",img)
            find_barcode(img)
            barcodes = []# check_barcode(img)

            if barcodes != []:
                return barcodes
        else:
            break

        ## adds a delay and escapes a video  - used only for debuggin
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
