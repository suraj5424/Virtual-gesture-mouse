
# 🖐️✨ Virtual Gesture Mouse — Documentation 🖱️🤖

---

## 🚀 Overview

**Virtual Gesture Mouse** lets you control your computer 🖥️ mouse cursor and clicks 🖱️ using simple hand gestures captured by your webcam 📸.  
Powered by **MediaPipe** 🤳 for hand tracking, **OpenCV** 🖼️ for video processing, **Autopy** 🐍 for mouse control, and **Streamlit** 🎨 for an interactive UI.

---

<img src="https://github.com/suraj5424/Virtual-gesture-mouse/blob/main/demo.gif" alt="Demo of Virtual Gesture Mouse" loop="infinite" />


---
## 📚 Table of Contents

- [🌟 Features](#-features)  
- [💻 System Requirements](#-system-requirements)  
- [⚙️ Installation](#%EF%B8%8F-installation)  
- [🎬 Usage](#-usage)  
- [🏗️ Application Architecture](#%EF%B8%8F-application-architecture)  
- [🧩 Core Components](#-core-components-explained)  
- [🔧 Configuration](#-configuration-parameters)  
- [🐞 Troubleshooting](#-troubleshooting)  
- [📄 License](#-license)  

---

## 🌟 Features

- 🤳 Real-time hand tracking with MediaPipe  
- 🖱️ Cursor movement controlled by your index finger  
- 👌 Mouse clicks by pinching thumb and index finger  
- ⚙️ Adjustable webcam resolution, frame margin, smoothing & click sensitivity  
- 👁️ Visual feedback: bounding boxes, landmarks, FPS display  
- 🖥️ Friendly, responsive UI built with Streamlit  

---

## 💻 System Requirements

- 🐍 Python 3.7+  
- 📸 Webcam (recommended min 640x480 resolution)  
- 💻 OS: Windows, macOS, or Linux  
- 🌐 Internet (for installing dependencies)  

---

## ⚙️ Installation

### Step 1: Clone the repo

```bash
git clone https://github.com/suraj5424/virtual-gesture-mouse.git
cd virtual-gesture-mouse
````

### Step 2: Setup virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate.bat    # Windows
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🎬 Usage

### Run the app

```bash
streamlit run app.py
```

* 🌐 Open the displayed URL (usually [http://localhost:8501](http://localhost:8501))
* 🎛️ Adjust settings in the sidebar (webcam size, smoothing, click threshold, etc.)
* ▶️ Click **Start Gesture Mouse** to begin controlling the mouse
* ⏹️ Click **Stop Gesture Mouse** to pause control

### Gesture Controls

| Gesture                       | Action            |
| ----------------------------- | ----------------- |
| ☝️ Index finger up            | Move mouse cursor |
| 🤏 Pinch thumb + index finger | Left mouse click  |

---

## 🏗️ Application Architecture

The app consists of two main parts:

### 1. `app.py` 🎨

* Streamlit UI and sidebar controls
* Webcam capture and video display
* Main gesture loop for detecting hand movement and controlling mouse
* Uses `gesturecontrol.py` for hand landmark processing

### 2. `gesturecontrol.py` 🧩

* `HandDetector` class leveraging MediaPipe Hands
* Hand detection, landmark extraction, and finger state analysis
* Utility functions:

  * `find_hands()` — detect & draw hands
  * `find_position()` — get landmark positions and bounding box
  * `find_distance()` — compute distance between landmarks
  * `finger_up()` — check which fingers are raised

---

## 🧩 Core Components Explained

### 🤳 Hand Detection

* MediaPipe Hands detects 21 landmarks per hand
* Tracks single hand for cursor control

### ✋ Gesture Recognition Logic

* Checks which fingers are up (1 = up, 0 = down)
* Index finger up → cursor moves
* Pinched thumb + index → mouse click

### 🖱️ Cursor Movement Mapping

* Maps webcam frame coords → screen coords
* Control frame margin restricts active area
* Movement smoothing avoids jitter

---

## 🔧 Configuration Parameters

| Parameter                          | Description                                    | Default | Range      |
| ---------------------------------- | ---------------------------------------------- | ------- | ---------- |
| 📷 Webcam Width (`wCam`)           | Video capture width                            | 640     | 400 - 1280 |
| 📸 Webcam Height (`hCam`)          | Video capture height                           | 480     | 300 - 720  |
| 🖼️ Control Frame Margin (`framR`) | Active area margin inside webcam frame         | 100     | 20 - 200   |
| 🌪️ Mouse Smoothing                | Smooth factor to reduce jitter                 | 7       | 1 - 15     |
| 🖱️ Click Threshold                | Max distance between thumb and index for click | 40      | 10 - 100   |

---

## 🐞 Troubleshooting

| Issue                          | Solution                              |
| ------------------------------ | ------------------------------------- |
| 🚫 Webcam not detected         | Check webcam connection & permissions |
| ✋ Gesture control unresponsive | Restart app; check hand visibility    |
| 🌀 Cursor moves erratically    | Increase smoothing value              |
| 👆 Clicks not registering      | Adjust click distance threshold       |

---

## 📄 License

This project is licensed under the [MIT License](LICENSE) — feel free to use and modify freely! 📝

---

## 📬 Contact

👨‍💻 Created by [Suraj Varma](https://www.linkedin.com/in/suraj5424/)
💻 GitHub: [suraj5424](https://github.com/suraj5424)

---

✨ Thanks for checking out **Virtual Gesture Mouse** — control your PC with a wave of your hand! ✋🖱️🚀
