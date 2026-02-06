# Like2Scroll

Like2Scroll is a simple computer-vision project that enables **scrolling control using hand gestures**.  
It uses a hand-landmark detection model together with Python to recognize gestures and translate them into scrolling actions.

---

## Features
- Real-time **hand landmark detection**
- Gesture-based **scroll interaction**
- Lightweight Python implementation
- Demo video included in the repository

---

## 📁 Project Structure
```
Like2Scroll/
│
├── main.py                # Main application script
├── hand_landmarker.task   # Hand landmark detection model
├── test.gif               # Demo video
└── README.md
```
The repository mainly consists of a Python script, a trained hand-landmarker model file, and a sample demo video. :contentReference[oaicite:1]{index=1}

---

## Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/doramonmon2306/Like2Scroll.git
cd Like2Scroll
```

### 2. Install dependencies
Install the required Python libraries (example):

```bash
pip install opencv-python mediapipe pynput
```

> Adjust dependencies if your local setup differs.

### 3. Run the project
```bash
python main.py
```

---

## Demo

Below is a short demonstration of the gesture-based scrolling system:

![](https://github.com/doramonmon2306/Like2Scroll/blob/main/demo.gif)

If the video does not load on GitHub preview, download and play **`test.gif`** locally from the repository.  
The demo file is included directly in the project files.

---

## How It Works
1. The webcam captures real-time hand movement.
2. A hand-landmark model detects finger positions.
3. Specific gestures are mapped to scrolling actions.
4. The system sends scroll commands to the operating system.

---

## Requirements
- Python 3.8+
- Webcam
- Supported OS: Windows / Linux / macOS

---

## Future Improvements
- More gesture commands (zoom, click, navigation)
- GUI interface
- Adjustable sensitivity and smoothing
- Cross-platform packaging

---

## License
This project is open-source.  
Add a license here if you plan to distribute it publicly.
