# Smart-Bridge
# TrafficTelligence: Advanced Traffic Volume Estimation with Machine Learning  

TrafficTelligence is an advanced system that leverages machine learning to estimate and predict traffic volume. It integrates **YOLOv7** for object detection and **Hough Transform** for lane detection, enabling real-time traffic analysis.  

## 🚀 Features  
- 🚗 **Object Detection**: Uses YOLOv7 to detect vehicles and other objects in traffic.  
- 🛣️ **Lane Detection**: Uses OpenCV and Hough Transform for accurate lane identification.  
- 📊 **Traffic Volume Prediction**: Analyzes historical data to estimate future traffic conditions.  
- ⚡ **Real-Time Insights**: Helps optimize traffic flow, urban planning, and commuter navigation.  

---

## 🔥 Project Scenarios  
### 1️⃣ Dynamic Traffic Management  
- Provides real-time traffic volume estimations.  
- Helps optimize signal timings and lane configurations.  

### 2️⃣ Urban Development Planning  
- Assists city planners in designing optimized road networks.  
- Supports infrastructure development based on traffic predictions.  

### 3️⃣ Commuter Guidance & Navigation  
- Helps navigation apps suggest better routes.  
- Assists commuters in avoiding traffic congestion.  

---

## 📥 Installation & Setup  

### 1️⃣ Clone the YOLOv7 Repository  
```bash
git clone https://github.com/WongKinYiu/yolov7.git  
cd yolov7

### 2️⃣ Install Dependencies
Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt

### 3️⃣ Add Provided Files
Copy the following files into the **YOLOv7** directory:

- 📜 `flaskaap.py` (Flask backend)
- 📜 `lane.py` (Lane detection script)
- 📜 `hubConfcustom.py` (YOLOv7 custom configurations)

Copy the following HTML files into the **templates** folder:

- 📄 `ui2.html`
- 📄 `indexproject.html`
- 📄 `videoprojectnew.html`

Modify these files to ensure correct **image paths** and **UI customization**.

### 4️⃣ Run the Application
After setting up the files, run the Flask application:

```bash
python flaskaap.py

Open your browser and navigate to:

http://127.0.0.1:5000/

### 📌 Usage
- Upload a traffic video or use a live stream.
- The system will detect lanes and objects in real time.
- View traffic volume estimations on the web interface.

### 🛠️ Technologies Used
- **YOLOv7**: Object detection
- **OpenCV**: Lane detection using Hough Transform
- **Flask**: Web framework
- **HTML/CSS**: UI design

### 🤝 Contributions
Feel free to contribute by submitting pull requests or reporting issues.

### 📜 License
This project is open-source under the **MIT License**.




