# **ISS - Intelligent Surveillance System using YOLO**

This project performs **fall detection, vehicle crash detection, and social distancing detection** from CCTV cameras in real-time using YOLO.

---

## **How YOLO Works?**

**YOLO (You Only Look Once)** is an object detection algorithm that processes an image only once, making it **fast and efficient** compared to R-CNN.

### **Steps in YOLO:**
1. **Divides the image** into a grid and generates multiple bounding boxes.
2. Assigns a **confidence score** to each bounding box based on object probability.
3. Selects **bounding boxes with high confidence scores** and eliminates overlapping ones.
4. Matches objects to the pre-trained **COCO dataset** (e.g., person, car, etc.).
5. **All predictions happen in a single forward pass**, making it fast.

---

## **Installation**

### **Software Requirements:**
- **Python**: Language used for the code
- **CMake**: Required for compiling OpenCV
- **Visual Studio Code**: For building OpenCV and Darknet
- **Nvidia GPU Driver**: For enhanced GPU performance
- **CUDA**: Parallel computing using GPU
- **CuDNN**: GPU-accelerated library for deep learning
- **OpenCV**: For image/video processing
- **Darknet**: YOLO's neural network framework

### **Installation Guide:**
Follow the **two-part YouTube tutorial** by [Augmented Startups](https://youtu.be/5pYh1rFnNZs?si=9vliNRIAcFzS3ldy).

> ⚠️ **Note:**
> - Use the **May 2020 - June 2020 version** of Darknet to avoid compatibility issues.
> - Check YouTube **comments** for error resolutions and download only the specified versions.

---

## **Usage**

Place your **Python files inside:**
```
YOLO\darknet\build\darknet\x64
```

### **Four Ways to Perform Detection:**
1. **Webcam**
2. **Locally Stored Video**
3. **YouTube Video**
4. **Mobile Camera (DroidCam)**

Edit the script to select the desired input source.

> ⚠ **Note:** For local videos, ensure they are inside `YOLO\darknet\build\darknet\x64` along with the script.

---

## **Features & Working**

### **1️⃣ Fall Detection**
- Converts video into frames.
- Converts frames to **black and white**.
- Detects **persons using YOLO**.
- Draws **bounding boxes** around detected persons.
- If the width of a box > height → **Fall Detected**.
- Alerts via **email** if a fall is detected in 20 consecutive frames.

> 📌 **Edit** `image_email_fall.py` to configure sender & receiver email.

#### **Running the script:**
```bash
python Fall_Detection.py
```

#### **Sample Output:**
![Fall Detection](https://github.com/Tejas-Keskar/Intelligent-Surveillance-System/blob/main/screenshots/Fall_Detection.jpg)

#### **Email Alert:**
![Fall Detection Email](https://github.com/Tejas-Keskar/Intelligent-Surveillance-System/blob/main/screenshots/Email_Fall_Detection.jpg)

---

### **2️⃣ Social Distancing Detection**
- Converts video into frames.
- Detects **persons using YOLO**.
- Measures the **distance** between each person.
- If distance < threshold → **Box turns Red (Violation Detected)**.
- Counts & displays total violations.

#### **Running the script:**
```bash
python Social_Distance.py
```

#### **Sample Output:**
![Social Distancing](https://github.com/Tejas-Keskar/Intelligent-Surveillance-System/blob/main/screenshots/Social_Distancing.jpg)

---

### **3️⃣ Vehicle Crash Detection**
- Converts video into frames.
- Detects **cars using YOLO**.
- If two cars are too close and bounding boxes overlap → **Crash Detected**.
- Alerts via **email** if a crash is detected in 20 consecutive frames.

> 📌 **Edit** `image_email_car.py` to configure sender & receiver email.

#### **Running the script:**
```bash
python Vehicle_Crash.py
```

#### **Sample Output:**
![Crash Detection](https://github.com/Tejas-Keskar/Intelligent-Surveillance-System/blob/main/screenshots/Crash_Detection.jpg)

#### **Email Alert:**
![Crash Detection Email](https://github.com/Tejas-Keskar/Intelligent-Surveillance-System/blob/main/screenshots/Email_Crash_Detection.jpg)

---

## **Project Deployment**

The project is deployed using **Flask**. Running the script **hosts a local website** where users can upload videos for detection.

#### **Running the script:**
```bash
python app.py
```

### **Website**
![ISS Webiste](https://github.com/Tejas-Keskar/Intelligent-Surveillance-System/blob/main/screenshots/ISS_Website.jpg)

---

## **Directory & File Structure**
```bash
darknet
|  
|───build
|   |
|   |───darknet
|   |	|
|   |	|───x64   
|   |	|   |───app.py
|   |	|   |───Fall_Detection.py
|   |	|   |───Object_Detection.py
|   |	|   |───Social_Distance.py
|   |	|   |───Vehicle_Crash.py
|   |	|   |───image_email.py
|   |	|   |
|   |	|   |───templates 
|   |	|   |   |───ContactUs.html
|   |	|   |   |───FallDetection.html
|   |	|   |   |───ObjectDetection.html
|   |	|   |   |───Shady.html
|   |	|   |   |───SocialDistancingDetection.html
|   |	|   |   |───VehicleCrashDetection.html
|   |	|   |   |───Video.html
|   |	|   |
|   |	|   |───static
|   |	|   |   |───assets
|   |	|   |   |───fonts
|   |	|   |   |───...files...
|   |	|   |───...files...
|   |   |───...files...	
|   |───...files...
|───...files...
```

---

## **Future Work**
- **Improve vehicle crash detection model**.
- **Deploy the website on Google Cloud** using **GPU acceleration** for global access.

---

## 📞 Contact  
If you have any questions or suggestions, feel free to reach out:  
📧 **Email:** keskartejas01@gmail.com  
📌 **LinkedIn:** https://www.linkedin.com/in/tejas-keskar-329634288

---

### **🔗 Useful Links**
- **YOLO Documentation:** [YOLO Docs](https://github.com/AlexeyAB/darknet)