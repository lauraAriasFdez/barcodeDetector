
# WEEKLY MEETINGS SCHEDULE
https://docs.google.com/document/d/1_nmwLH6sHvKKXILZZlrdr-wn2X0gufjl75-ZsQqTDrs/edit


# REQUIREMENTS TO RUN YOLOV5 ON YOUR COMPUTER (make sure to be in yolov5-master folder directory)
cuda
pythorch 
pip install requirements.txt

# COMMAND TO RUN YOLOV5 model on camera
(basic model of yolo): python detect.py --source 0
(my barcode detector yolov5): python detect.py --source 0 --weights barcode_model.pt

# PROGRESS TO NOTE
- edgde_detect_barcode.py not really working as it is not reliable
- yolov5 model started on BARCODE_SCANNER.ipynb  (barcode_model.pt downloaded from there)
