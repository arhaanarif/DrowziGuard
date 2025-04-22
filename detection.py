import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
from scipy.spatial import distance as dist
import pygame
import threading
import time
import uuid

# Constants
MODEL_PATH = r"Models\model224.h5"
LABELS = ["Non-Drowsy", "Drowsy"]
MODEL_INPUT_SIZE = (224, 224)  # MobileNetV2 input size

class DrowsinessDetector:
    def __init__(self, model_path=MODEL_PATH):
        self.model = tf.keras.models.load_model(model_path)
        self.running = False

        # Initialize MediaPipe FaceMesh
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.left_eye_indices = [33, 160, 158, 133, 153, 144]  # Left eye landmarks
        self.right_eye_indices = [362, 385, 387, 263, 373, 380]  # Right eye landmarks
        self.closed_eyes_start_time = None
        self.blink_threshold = 0.25  # Adjusted for better sensitivity
        self.blink_duration_threshold = 3.5  # 3-4 seconds
        self.warning_start_time = None
        self.warning_duration = 5  # 5-second warning display
        self.alert_cooldown = 2  # Reduced to allow frequent alerts
        self.last_alert_time = 0

        # Initialize pygame mixer
        pygame.mixer.init()

    def preprocess_frame(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, MODEL_INPUT_SIZE)
        normalized = resized / 255.0
        return np.expand_dims(normalized, axis=0)

    def predict_status(self, frame):
        processed_frame = self.preprocess_frame(frame)
        prediction = self.model.predict(processed_frame, verbose=0)[0]
        
        if len(prediction) != 4:
            print(f"❌ Model output shape mismatch! Expected 4, got {len(prediction)}")
            return "Unknown"
        
        class_idx = np.argmax(prediction)
        if class_idx in [0, 3]:
            return LABELS[0]  # Non-Drowsy
        elif class_idx in [1, 2]:
            return LABELS[1]  # Drowsy
        return "Unknown"

    def calculate_EAR(self, eye_points):
        A = dist.euclidean(eye_points[1], eye_points[5])
        B = dist.euclidean(eye_points[2], eye_points[4])
        C = dist.euclidean(eye_points[0], eye_points[3])
        ear = (A + B) / (2.0 * C)
        return ear

    def detect_eye_closure(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)
        if not results.multi_face_landmarks:
            self.closed_eyes_start_time = None
            return False

        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = frame.shape
            left_eye = [
                (face_landmarks.landmark[i].x * w, face_landmarks.landmark[i].y * h)
                for i in self.left_eye_indices
            ]
            right_eye = [
                (face_landmarks.landmark[i].x * w, face_landmarks.landmark[i].y * h)
                for i in self.right_eye_indices
            ]

            left_ear = self.calculate_EAR(left_eye)
            right_ear = self.calculate_EAR(right_eye)
            ear = (left_ear + right_ear) / 2.0

            current_time = time.time()
            if ear < self.blink_threshold:
                if self.closed_eyes_start_time is None:
                    self.closed_eyes_start_time = current_time
                elif current_time - self.closed_eyes_start_time >= self.blink_duration_threshold:
                    return True
            else:
                self.closed_eyes_start_time = None
            return False

    def play_alert(self):
        try:
            print("Playing alert sound...")
            pygame.mixer.music.load("Assets/alert2.mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
        except Exception as e:
            print(f"Error playing alert: {e}")

    def display_frame(self, frame, status, warning=None):
        color = (0, 255, 0) if "Non-Drowsy" in status else (0, 0, 255)
        cv2.putText(frame, f"Status: {status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        if warning:
            cv2.rectangle(frame, (0, 50), (frame.shape[1], 100), (0, 0, 255), -1)  # Red background for visibility
            cv2.putText(frame, warning, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.imshow("Drowsiness Detection", frame)

    def run(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return

        self.running = True
        while self.running:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            frame = cv2.flip(frame, 1)
            current_time = time.time()

            # Model-based drowsiness detection
            drowsy_by_model = self.predict_status(frame) == "Drowsy"
            # Eye closure detection
            eyes_closed_long = self.detect_eye_closure(frame)

            status = "Non-Drowsy"
            warning_msg = None
            if drowsy_by_model or eyes_closed_long:
                status = "Drowsy" if drowsy_by_model else "Drowsy (Eyes Closed)"
                if current_time - self.last_alert_time > self.alert_cooldown:
                    warning_msg = "⚠️ Drowsiness Detected! Stay Alert for 5s"
                    self.warning_start_time = current_time
                    self.last_alert_time = current_time
                    threading.Thread(target=self.play_alert, daemon=True).start()
                elif self.warning_start_time and (current_time - self.warning_start_time <= self.warning_duration):
                    warning_msg = "⚠️ Drowsiness Detected! Stay Alert for 5s"

            self.display_frame(frame, status, warning_msg)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.running = False
        cap.release()
        cv2.destroyAllWindows()
        self.face_mesh.close()
        pygame.mixer.quit()

    def stop(self):
        self.running = False

def detection():
    detector = DrowsinessDetector()
    detector.run()

if __name__ == "__main__":
    detection()