import cv2
import time

## Global
timeout_video = 60

## draw barcode - find barcodes (drawing contours -faster speed, 
                                # opencv only supports ean13 https://docs.opencv.org/4.x/d6/d25/tutorial_barcode_detect_and_decode.html
                                # yolo object detection)
# check if barcode can be decoded
# if cannot and its a barcode, find why, showing too little, need to zoom?

# https://laconicml.com/barcode-detection-opencv/
# https://www.pyimagesearch.com/2014/12/15/real-time-barcode-detection-video-python-opencv/
# https://www.youtube.com/channel/UCP_ojiChHCQN-vKIMtNA6rw/featured
def find_barcode(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gradX = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=-1)
    gradY = cv2.Sobel(gray, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=-1)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)
    blurred = cv2.blur(gradient, (9, 9))

    ret,thresh = cv2.threshold(blurred,225,255,cv2.THRESH_BINARY)

    # construct a closing kernel and apply it to the thresholded image
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 7)) #21,7
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)

    # find the contours in the thresholded image
    cnts,_ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #i = sorted(cnts,key=cv2.contourArea,reverse=True)[0]
    #cv2.drawContours(image,[i],-1,(0,255,0),3)
    cv2.drawContours(image,cnts, -1, (0,255,0),3)

    cv2.imshow("img1",image)


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

video_capture()