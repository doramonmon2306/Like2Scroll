import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
from queue import Queue
import pyautogui
import threading
import time

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),        # Index
    (0, 9), (9, 10), (10, 11), (11, 12),   # Middle
    (0, 13), (13, 14), (14, 15), (15, 16), # Ring
    (0, 17), (17, 18), (18, 19), (19, 20), # Pinky
    (5, 9), (9, 13), (13, 17)              # Palm connections
]

frame_queue = Queue(maxsize=2)
current_gesture = None
gesture_lock = threading.Lock()
scroll_thread = None
stop_scroll = threading.Event()

def to_pixel(x_norm: float, y_norm: float, w: int, h: int):
    x = min(max(x_norm, 0.0), 1.0)
    y = min(max(y_norm, 0.0), 1.0)
    return int(x * w), int(y * h)

def draw_hand_landmarks(image, hand_landmarks):
    global current_gesture, scroll_thread
    h, w, _ = image.shape
    
    for connection in HAND_CONNECTIONS:
        start_idx, end_idx = connection
        start_landmark = hand_landmarks[start_idx]
        end_landmark = hand_landmarks[end_idx]
        start_x, start_y = to_pixel(start_landmark.x, start_landmark.y, w, h)
        end_x, end_y = to_pixel(end_landmark.x, end_landmark.y, w, h)
        cv2.line(image, (start_x, start_y), (end_x, end_y), color=(255, 255, 255), thickness=2)
    
    for idx, landmark in enumerate(hand_landmarks):
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        cv2.circle(image, center=(x, y), radius=5, color=(0, 0, 0), thickness=-1)  

def finger_close(landmarks, finger_tip_idx, finger_pip_idx, wrist_idx=0):
    tip = landmarks[finger_tip_idx]
    pip = landmarks[finger_pip_idx]
    wrist = landmarks[wrist_idx]
    tip_to_wrist_x = abs(tip.x - wrist.x)
    pip_to_wrist_x = abs(pip.x - wrist.x)
    
    return tip_to_wrist_x > pip_to_wrist_x 

def thumb_check(landmarks):
    thumb_tip = landmarks[4]
    thumb_mcp = landmarks[2]
    vertical_distance = abs(thumb_tip.y - thumb_mcp.y)
    horizontal_distance = abs(thumb_tip.x - thumb_mcp.x)
    return vertical_distance > horizontal_distance

def detect_gesture(landmarks):
    fingers_extended = [
        finger_close(landmarks, 8, 6),
        finger_close(landmarks, 12, 10),
        finger_close(landmarks, 16, 14),
        finger_close(landmarks, 20, 18)
    ]
    
    thumb_extended_vertical = thumb_check(landmarks)
    
    if thumb_extended_vertical and not any(fingers_extended):
        if landmarks[4].y < landmarks[2].y + 0.05:  
            return "LIKE"
        elif landmarks[4].y > landmarks[2].y + 0.05:  
            return "DISLIKE"
    
    return None


def continuous_scroll(direction):
    scroll_amount = -6 if direction == "LIKE" else 6
    
    while not stop_scroll.is_set():
        pyautogui.scroll(scroll_amount)
        time.sleep(0.05)

def hand_result_callback(result: vision.HandLandmarkerResult, output_image: mp.Image, timestamp_ms: int):
    global current_gesture, scroll_thread
    annotated_image = output_image.numpy_view().copy()
    detected_gesture = None
    
    if result.hand_landmarks:
        hand_landmarks = result.hand_landmarks[-1]
        draw_hand_landmarks(annotated_image, hand_landmarks)
        detected_gesture = detect_gesture(hand_landmarks)

    with gesture_lock:
        if detected_gesture != current_gesture:
            if scroll_thread and scroll_thread.is_alive():
                stop_scroll.set()
                scroll_thread.join(timeout=0.1)
            
            if detected_gesture:
                print(f"{'LIKE - Scrolling DOWN' if detected_gesture == 'LIKE' else 'DISLIKE - Scrolling UP'}")
                stop_scroll.clear()
                scroll_thread = threading.Thread(target=continuous_scroll, args=(detected_gesture,), daemon=True)
                scroll_thread.start()
            else:
                print("Stopped scrolling")
            
            current_gesture = detected_gesture
    
    display_image = cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR)
    timestamp_text = f"Time: {timestamp_ms}ms | Hands: {len(result.hand_landmarks) if result.hand_landmarks else 0}"
    (text_width, text_height), baseline = cv2.getTextSize(timestamp_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
    cv2.rectangle(display_image, (10, 10), (15 + text_width, 15 + text_height), color=(255, 255, 255), thickness=-1)
    cv2.putText(display_image, text=timestamp_text, org=(15, 15 + text_height), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.5, color=(0, 0, 0), thickness=2)

    if not frame_queue.full():
        frame_queue.put(display_image)
def run_webcam():
    global scroll_thread
    
    base_options = python.BaseOptions(model_asset_path='hand_landmarker.task')
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.LIVE_STREAM,
        num_hands=2, 
        min_hand_detection_confidence=0.5,
        min_hand_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        result_callback=hand_result_callback
    )
    
    landmarker = vision.HandLandmarker.create_from_options(options)
    cap = cv2.VideoCapture(0)
    timestamp = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        landmarker.detect_async(mp_image, timestamp)
        
        if not frame_queue.empty():
            display_image = frame_queue.get()
            cv2.imshow('Hand Landmark Detection', display_image)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        
        timestamp += 33
    
    stop_scroll.set()
    if scroll_thread and scroll_thread.is_alive():
        scroll_thread.join(timeout=0.5)
    
    cap.release()
    cv2.destroyAllWindows()
    landmarker.close()

if __name__ == "__main__":
    run_webcam()