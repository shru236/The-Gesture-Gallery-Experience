# We import the necessary modules for video processing, array manipulation, gesture detection and the Machine Learning model.
import cv2
import numpy as np
import mediapipe as mp
import pickle

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
    def detect_and_log(self, image, frame_idx: int) -> str:
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
                # We flatten the landmark array and predict the gesture using the loaded model.
                landmarks = np.array(landmarks).flatten().reshape(1, -1)
                gesture_category = self.model.predict(landmarks)[0]
                # We draw the landmarks of the hand on the image using mediapipe.
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

        # We add the detected gesture to the gesture history and keep its size to a maximum of 5.
        self.gesture_history.append(gesture_category)
        if len(self.gesture_history) > 5:
            self.gesture_history.pop(0)

        # We determine the most frequent gesture and return it.
        final_gesture = self.get_most_common_gesture()
        return final_gesture

    # Function to determine the most frequent gesture from the gesture history.
    def get_most_common_gesture(self):
        if not self.gesture_history:
            return "None"
        return max(set(self.gesture_history), key=self.gesture_history.count)
