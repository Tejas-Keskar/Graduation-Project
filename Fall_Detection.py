#================================================================ 
from ctypes import *
import math
import random
import os
import cv2
import numpy as np
import time
import darknet
from itertools import combinations
import pafy
import youtube_dl
import image_email_fall  # Uncomment for alert to email
from datetime import datetime
import mysql.connector

def convertBack(x, y, w, h): 
    #================================================================
    # Purpose : Converts center coordinates to rectangle coordinates
    #================================================================  
    """
    :param:
    x, y = midpoint of bbox
    w, h = width, height of the bbox
    
    :return:
    xmin, ymin, xmax, ymax
    """
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

alert_var = 0     # Uncomment for alert to email     # makes sure that alert (Sending an E-mail) is generated only once

def cvDrawBoxes(detections, img):
    """
    :param:
    detections = total detections in one frame
    img = image from detect_image method of darknet

    :return:
    img with bbox
    """
    global alert_var   # Uncomment for alert to email
    
    #================================================================
    # Purpose : Filter out Persons class from detections
    #================================================================
    if len(detections) > 0:  						# At least 1 detection in the image and check detection presence in a frame  
        centroid_dict = dict() 						# Function creates a dictionary and calls it centroid_dict
        objectId = 0								# We inialize a variable called ObjectId and set it to 0
        for detection in detections:				# In this if statement, we filter all the detections for persons only
            # Check for the only person name tag 
            name_tag = str(detection[0])   # Coco file has string of all the names
            if name_tag == 'person':                
                x, y, w, h = detection[2][0],\
                            detection[2][1],\
                            detection[2][2],\
                            detection[2][3]      	# Store the center points of the detections
                xmin, ymin, xmax, ymax = convertBack(float(x), float(y), float(w), float(h))   # Convert from center coordinates to rectangular coordinates, We use floats to ensure the precision of the BBox            
                # Append center point of bbox for persons detected.
                centroid_dict[objectId] = (int(x), int(y), xmin, ymin, xmax, ymax) # Create dictionary of tuple with 'objectId' as the index center points and bbox
    #=================================================================#
    
    #=================================================================
    # Purpose : Determine whether the fall is detected or not 
    #=================================================================            	
        fall_alert_list = [] # List containing which Object id is in under threshold distance condition. 
        red_line_list = []
        for id,p in centroid_dict.items():
            dx, dy = p[4] - p[2], p[5] - p[3]  	# Check the difference
            difference = dy-dx			
            if difference < 0:						
                fall_alert_list.append(id)       #  Add Id to a list
        
        for idx, box in centroid_dict.items():  # dict (1(key):red(value), 2 blue)  idx - key  box - value
            if idx in fall_alert_list:   # if id is in red zone list
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (255, 0, 0), 2) # Create Red bounding boxes  #starting point, ending point size of 2
            else:
                cv2.rectangle(img, (box[2], box[3]), (box[4], box[5]), (0, 255, 0), 2) # Create Green bounding boxes
		#=================================================================#

		#=================================================================
    	# Purpose : Displaying the results and sending an alert message
    	#================================================================= 
        if len(fall_alert_list)!=0:
            text = "Fall Detected"
            
            #Uncomment the below lines for alert to email
            if alert_var == 20:         # makes sure that alert is generated when there are atleast 20 frames which shows that a fall has been detected
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
                cv2.imwrite('fall_alert.jpg',img)
                image_email_fall.SendMail('fall_alert.jpg')
            alert_var += 1;
            
        else:
            text = "Fall Not Detected"
            alert_var = 0           # makes sure that alert is generated when there are 20 simultaeous frames of fall detection
            
        location = (10,25)												# Set the location of the displayed text
        if len(fall_alert_list)!=0:
            cv2.putText(img, text, location, cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)  # Display Text
        else:
            cv2.putText(img, text, location, cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2, cv2.LINE_AA)  # Display Text

        #=================================================================#
    return img





def YOLO():

    mail1=input("Enter Email for notification:")
    now = datetime.now()
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')

    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="fall"
    )

    mycursor = mydb.cursor()

    sql = "INSERT INTO email (mail,date) VALUES (%s,%s)"
    val = (mail1,formatted_date)
    mycursor.execute(sql,val)

    mydb.commit()
    """
    Perform Object detection
    """
   
    configPath = "./cfg/yolov4.cfg"                                 # Path to cfg
    weightPath = "./yolov4.weights"                                 # Path to weights
    metaPath = "./cfg/coco.data"                                         # Path to meta data
    network, class_names, class_colors = darknet.load_network(configPath,  metaPath, weightPath, batch_size=1)
            
    #cap = cv2.VideoCapture(0)                                           # Uncomment to use Webcam
    
    #cap = cv2.VideoCapture("falling.mp4")                                # Uncomment for Local Stored video detection - Set input video
    #cap = cv2.VideoCapture("falling.mp4")
    #cap = cv2.VideoCapture("fall-3.mp4")
    #cap = cv2.VideoCapture("Fall-Detection-Original.mp4")
    
    url = "https://www.youtube.com/watch?v=8Rhimam6FgQ"                 # Uncomment these lines for video from youtube
    video = pafy.new(url)
    best = video.getbest(preftype="mp4")
    cap = cv2.VideoCapture()
    cap.open(best.url)    
    
    #cap = cv2.VideoCapture('http://192.168.45.250:4747/video')       # Uncomment for Video from Mobile Camera (DroidCam Hosted Camera)
    
    frame_width = int(cap.get(3))                                        # Returns the width and height of capture video   
    frame_height = int(cap.get(4))
    new_height, new_width = frame_height // 2, frame_width // 2
    #print("Video Reolution: ",(width, height))

    out = cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"MJPG"), 10.0,  # Uncomment to save the output video   # Set the Output path for video writer
            (new_width, new_height))
    
    print("Starting the YOLO loop...")

    # Create an image we reuse for each detect
    darknet_image = darknet.make_image(new_width, new_height, 3)         # Create image according darknet for compatibility of network
    
    while True:                                                          # Load the input frame and write output frame.
        prev_time = time.time()
        ret, frame_read = cap.read()                                   
        # Check if frame present :: 'ret' returns True if frame present, otherwise break the loop.
        if not ret:
            break

        frame_rgb = cv2.cvtColor(frame_read, cv2.COLOR_BGR2RGB)          # Convert frame into RGB from BGR and resize accordingly
        frame_resized = cv2.resize(frame_rgb,
                                   (new_width, new_height),
                                   interpolation=cv2.INTER_LINEAR)

        darknet.copy_image_from_bytes(darknet_image,frame_resized.tobytes())    # Copy that frame bytes to darknet_image

        detections = darknet.detect_image(network, class_names, darknet_image, thresh=0.25)    # Detection occurs at this line and return detections, for customize we can change
        image = cvDrawBoxes(detections, frame_resized)                   # Call the function cvDrawBoxes() for colored bounding box per class
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        print(1/(time.time()-prev_time))                             # Prints frames per second
        cv2.imshow('Demo', image)                                    # Display Image window
        cv2.waitKey(3)
        #out.write(image)                                            # Write that frame into output video
        
    cap.release()                                                    # For releasing cap and out. 
    #out.release()                                                   # Uncomment to save the output video 
    print(":::Video Write Completed")

if __name__ == "__main__":
    YOLO()                                                           # Calls the main function YOLO()
