
<a href="https://www.linkedin.com/in/laura-arias-fernandez-61b121191/">
    <img align="left" src="https://github.com/lauraAriasFdez/lauraAriasFdez/blob/main/linkedin.png" alt="LinkedIn" width="21px"/>                                                   
</a>

<a href="mailto:larfer2001@gmail.com">
    <img align="left" src="https://github.com/lauraAriasFdez/lauraAriasFdez/blob/main/email.png" alt="Email" width="25px"/>                                                   
</a>

By Laura Arias Fernandez

Project Created as part of my Undergraduate Research (UMN UROP)

Faculty Mentor: Maria Gini

[Research Paper](./UROP_Paper.pdf)

[Research Poster](./Research_Poster.png)

[Demo](https://www.youtube.com/watch?v=z4ixJT4SuLI)


# Overview
The aim of the project is to develop a robust program that aids visually impared individuals shop at a grocery store. More specifically, the goal is to develop two different tools: (1) a barcode scanner, such that when a product is scanned the user can hear the different ingredients of the product through a speech interface, and (2) an object recognition interface that is able to distinguish between different grocery items, and indicates to the user which product is in front of them. 

### (1) a barcode scanner
In order to build the product information software via barcode scanner. A  deep learning based framework, yolov5, was used to design a barcode object detector, and a convolutional neural network was trained on a dataset of approximately 1500 annotated barcode images from a publicly available dataset in Kaggle. The barcode detector was used to provide for a more robust barcode scanner software. In order for the camera to accurately scan a barcode, the barcode needs to be very close to the camera, which can be very difficult for visually impared individuals to do. This object detector allows the camera to locate a barcode in a muddled area. It minimizes the need for the visually impaired user to be very close to a product in order to recognize the barcode. The system is designed to detect barcodes and assists the user by directing them through verbal instructions on where and how to move their camera to successfully scan the barcode.

The proposed model was able to detect barcodes (class = 1) accurately with 100% recall (percentage of barcodes correctly identified) and a 98% precision (percentage of correct predictions). 

The software integrates a web-scraping technique using the Python Library BeautifulSoup to collect product information data. This data is gathered from an open source database called Open Food Facts which has information in regards to ingredients, nutritional information, name, possible allergies and quantity information of over 2 million products across the globe. Thereby, once the software was able to obtain the EAN number, web scraping was used on the Open Food Facts to gather information about the product. To provide assistance to the blind, this information is read by the software out loud to them. 


### (2) Grocery Items Object Recognition  

The second part of this software is object recognition. To recognize many different types of objects, to provide "visual assistance" to the blind, i.e. identify objects in their surroundings, and then tell them what they are. The neural network was built using yolov4, and trained to classify the following object classes:

                  Fruit   Pastry    Pasta     Coffee    Toilet paper

                  Bread   Milk      Salad     Flower    Popcorn

                  Fish   Juice      Sandwich  Sushi     Ice cream

                  Candy  Vegetable  Cheese    Cookie    Cooking spray

                  Tea


 For each of the classes, we gathered a dataset from Open Images, a dataset of ~9M images annotated with image-level labels from Google. We then converted the annotations to the desired format, and used it to start training. Training a neural network of such dimensions is very challenging, and in order to do so I made use of Google codelab, a platform that allows to train the neural networks in s GPU, rather than the CPU of the computer. By leveraging Codelab resources, I was able to accelerate training by saving checkpoints every hour. This task can still take a lot of time, and by the time writing this report training has still not finished, but as figure 3.0 shows we can see slight performance of the neural network.

 [Object Detection Images Examples](./yolov4-groceries/img/)
 [Object Detection Weights](./yolov4-groceries/weights/)
Note: I have only uploded the last weights, the best weights and the last iteration saved (80000) to this github repository.
[Dataset Files](./yolov4-groceries/dataset/)
Note: The zip files containing the dataset are not uploaded due to its large size. Email me if needed. 

# What is in this directory?

<ul>
  <li>  <code>README.md</code>

  <li>  <code>yolov5-codelab</code> folder, which contains google codelab notebook showing the barcode object detector training. 
      - Such training produce barcode_model.pt weights foind in barcode_detector folder

  <li>  <code>yolov5-master</code> folder, which contains source code to run barcode detector on camera 
      - Not really use directly in this program but very useful for concept proving. 

  <li>  <code>yolov4-groceries</code> folder, which contains google codelab notebook showing the groceries object detector training. 
      - All training is saved in my google drive 

  <li>  <code>barcode_detector</code> folder which contains the implementation of my project as described in the overivew section. 

</ul>


# Requirements to Run Yolov5

- cuda
- pythorch 
- pip3 install -r yolov5-master/requirements.txt

```
pip install zbarcam
pip install opencv-python
pip install pyzbar
pip intall numpy 

pip install SpeechRecognition
pip install gtts
pip install pyttsx3
pip install PyAudio
pip install playsound

pip install beautifulsoup4
pip install lxml 
pip install requests 

```
(Note that you may need to manually download pyaudio executable since the pip command contains errors)


# Getting Started 

```
cd barcode_detector
python main.py

```

### Command to Run Only YoloV5 model on camera

  - (basic model of yolo): 
      
      ```
      cd yolov5-master
      python detect.py --source 0
      ```

- (my barcode detector yolov5):
      ```
      cd yolov5-master
      python detect.py --source 0 --weights barcode_model.pt
      ```

# Progress to Note
 1. barcode_detector/Trial_not_success contains 
    - edgde_detect_barcode.py:  not really working as it is not reliable
    - other_decoder.py : exactly as efficient as pzlibrary use for obtaining ean number of barcodes

Although the design of the product information software was very robust, a lot of room for improvement remains. The experimental results proved that the computation could be better made to tell the user where to move the camera to in order to scan the barcode. Furthermore, although through aid, it is still necessary to bring the barcode very close to the camera to be scanned effectively. The barcode object detector could be improved so that it would not only detect but also scan the barcode when the object is further away. 

Moreover, the results for the object recognition were not as intended. I used a convolutional neural network to automatically learn a representation of each object class. The dataset was very large, with thousands of images per class. Training a neural network of such dimensions is very challenging, and such tasks can still take a lot of time.  After hours of training we can see that the neural network has started recognizing some objects (Figure 3.0). Yet, as seen from figure 3.1 there are still some errors in the object recognition, and more training time needs to occur in order to accurately evaluate the performance of the object recognition. 



# Resources Explored (Not Necessary Used All)

### Barcode Object Detector
1. Kaggle DATASET: https://www.kaggle.com/whoosis/barcode-detection-annotated-dataset)

    a) Augmentations added: brightness, flip and 90degree rotation

    b) Dataset has been uploaded to [Roboflow](https://roboflow.ai) for annotation and augmentation
        - https://app.roboflow.com/new-workspace-vlbun/barcodedetection-v2/1
        
2. [EXPLANATION](https://github.com/ultralytics/yolov5/wiki/Train-Custom-Data) of how to train custom yolov5

### Grocery item deteciton: 
1. http://students.washington.edu/bhimar/highlights/2020-12-18-GrocerEye/
2. Dataset: 
    - Frieburg grocery dataset https://paperswithcode.com/dataset/freiburg-groceries
    - https://paperswithcode.com/dataset/grocery-store
    - https://github.com/glovo/foodi-ml-dataset  (not the best as we need aws)
    - https://storage.googleapis.com/openimages/web/index.html (could download 30 or 40 classes of product and training them) - USED
### Darknet (Yolov4)
    - https://pjreddie.com/darknet/install/


