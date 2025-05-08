# DrowziGuard AI – Driver Drowsiness Detection System

**DrowziGuard** is a safety-critical application designed to monitor and detect signs of driver fatigue in real-time. By leveraging computer vision and machine learning, the system analyzes facial features, eye movements, and head posture to identify drowsiness indicators, issuing timely alerts to prevent accidents caused by impaired driving.

---

## Overview

Drowsiness while driving is a major cause of road accidents. DrowziGuard AI uses a convolutional neural network (CNN) model integrated with OpenCV to monitor the driver’s eye and yawning state via webcam. If drowsiness is detected, the system triggers visual and audible alerts to wake the driver to take corrective actions.

---

## Features

- **Real time Monitoring:** Continuously analyzes video input for signs of drowsiness
- **Eye Aspect Ratio Analysis:** Measures eye closure duration to detect prolonged blinks or closed eyes.
- **Alert System:** Emits audio and visual warning when drowsiness is detected.

---

## How It Works

1. **Capture**: Real-time video stream using the system webcam.
2. **Detection**: Face and eye detection using OpenCV Haar cascades.
3. **Prediction**: A CNN model classifies whether eyes are open or closed.
4. **Drowsiness Logic**: If eyes are closed beyond a set threshold duration, an alert is triggered.
5. **Alert**: Emits sound and shows alert on screen (optionally sends SMS).

---

## Hardware Requirements

- **Camera:** Webcam or USB camera with at least 640x480 resolution and 30 FPS.
- **Processor:** Minimum 2 GHz dual-core CPU (Intel i5 or equivalent recommended).
- **RAM:** At least 4 GB (8 GB recommended for smooth performance)
- **Storage:** 500 MB free space for models and dependencies.
- **Speaker:** For audio alerts.
- **GPU:** Optional but recommended for faster model inference NVIDIA GPU with CUDA support

---

## Software Requirements

- **Operating System:** Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)
- **Python:** Version 3.9 or higher.
- **Python Packages** (listed in requirements.txt):
  Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
python==3.9
tensorflow==2.8
opencv-python==4.10.0
dlib==19.24.2
numpy==1.26.4
scipy==1.13.1
playsound==1.3.0
streamlit==1.10
```

---

## Installation

- \*\*Clone the Repository:

```bash
git clone https://github.com/arhaanarif/DrowziGuard.git
```

- **Setup Virtual Environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

- **Install Dependencies:**

```bash
pip install -r requirements.txt
```

---

## Limitations

- **Lighting Conditions:** Performance may degrade in low-light or extreme lighting.
- **Camera Angle:** Requires the camera to face the driver directly.
- **Occlusions:** Glasses, hates or excessive facial hair may affect detection accuracy.
- **Processing Speed:** Real-time performance depends on hardware capabilities.

---

## Usage

- Ensure the camera is connected and positioned to capture the dirver's face
- Run main.py to start the system
