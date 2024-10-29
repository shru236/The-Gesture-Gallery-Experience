# We import the necessary modules for video processing, array manipulation, gesture detection and the Machine Learning model.
import cv2
import numpy as np
import mediapipe as mp
import pickle
import itertools
import tqdm
from sklearn.svm import SVC

# We define the GestureDetectorLogger class for gesture detection and logging.
class GestureDetectorLogger:
    def __init__(self, video_mode: bool = False):
        # We initialize the video mode.
        self._video_mode = video_mode

        # We load the trained gesture model from the file.
        with open('gesture_model.pkl', 'rb') as f:
            self.model = pickle.load(f)

        # We initialize the history of gestures and their labels.
        self.gesture_history = []
        self.gesture_labels = ['Next', 'Previous', 'OK', 'Victory', 'Like', 'Dislike', 'Open Palm', 'Closed Palm']

        # We initialize the mediapipe for hand detection.
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils

    # Feature for detecting and logging gestures in an image.
    def detect_and_log(self, image, frame_idx: int) -> None:
        # We get the dimensions of the image and convert it to RGB.
        height, width, _ = image.shape
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)

        gesture_category = "None"
        # If hands were detected, we extract the coordinates of the landmarks and predict the gesture.
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.append([lm.x, lm.y, lm.z])
                landmarks = np.array(landmarks).flatten().reshape(1, -1)
                gesture_category = self.model.predict(landmarks)[0]
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        # We add the detected gesture to the gesture history and keep its size to a maximum of 5.
        self.gesture_history.append(gesture_category)
        if len(self.gesture_history) > 5:
            self.gesture_history.pop(0)

        # We determine the most frequent gesture and display it on the image.
        final_gesture = self.get_most_common_gesture()
        self.draw_gesture_indicator(image, final_gesture)
        print("Gesture Category:", final_gesture)

    # Function to draw the gesture indicator on the image.
    def draw_gesture_indicator(self, image, gesture_name):
        cv2.putText(image, f"Gesture: {gesture_name}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Function to determine the most frequent gesture from the gesture history.
    def get_most_common_gesture(self):
        if not self.gesture_history:
            return "None"
        return max(set(self.gesture_history), key=self.gesture_history.count)

# Function to run the application using the webcam.
def run_from_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    detector = GestureDetectorLogger(video_mode=True)

    try:
        it = itertools.count()
        # We process the video frames using tqdm to display the progress.
        for frame_idx in tqdm.tqdm(it, desc="Processing frames"):
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame from webcam.")
                break

            # We convert the frame to RGB and detect the gestures.
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            detector.detect_and_log(frame_rgb, frame_idx)

            # We display the frame with the detected gestures.
            cv2.imshow('Real-Time Gesture Recognition', cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        cap.release()
        cv2.destroyAllWindows()

# If the file is run directly (not imported as a module), we call the run_from_webcam function to start the application.
if __name__ == "__main__":
    run_from_webcam()
