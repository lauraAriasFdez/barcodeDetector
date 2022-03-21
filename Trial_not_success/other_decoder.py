#import libraries
from re import L
import cv2
from pyzbar import pyzbar

import numpy as np
#python -m pip install -U scikit-image
from skimage import io      # Only needed for web grabbing images, use cv2.imread for local images

"""
https://github.com/Barmaley13/barcap
https://pypi.org/project/barcap/
"""
def transform_frame(frame):

    # Read image from web, convert to grayscale, and inverse binary threshold
    image = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    _, image_thr = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY_INV)

    # Count non-zero pixels along the rows; get indices, where count exceeds certain threshold (here: 100)
    row_nz = np.count_nonzero(image_thr, axis=0)
    idx = np.argwhere(row_nz > 100)

    # Generate new image, draw lines at found indices
    image_new = np.ones_like(image_thr) * 255
    image_new[35:175, idx] = 0

    #cv2.imshow('image_thr', image_thr)
    #cv2.imshow('image_new', image_new)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    return image_new

def read_barcodes(frame):
    #transform_frame(frame)
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y , w, h = barcode.rect
        #1
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
        
        #2
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
        #3
        with open("barcode_result.txt", mode ='w') as file:
            file.write("Recognized Barcode:" + barcode_info)
    return frame

def main2():
    #1
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    #2
    while ret:
        ret, frame = camera.read()
        frame = read_barcodes(frame)
        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    #3
    camera.release()
    cv2.destroyAllWindows()
#4

def main ():
    from barcap.barcode import BarcodeCapture     
    capture = BarcodeCapture(camera=0)
    capture.start()
    while (True):
        if capture.new:
            print(f'output: {capture.output}')


if __name__ == '__main__':
    main()


    