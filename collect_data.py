# We import the necessary modules for video capture, image processing and data serialization.
import cv2
import mediapipe as mp
import pickle

# We initialize the hand detection solution in Mediapipe.
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# We define the list of gestures that will be collected.
gestures = ['Next', 'Previous', 'OK', 'Victory', 'Like', 'Dislike', 'Open Palm', 'Closed Palm']

# We create a dictionary to store the data for each gesture.
gesture_data = {gesture: [] for gesture in gestures}

# We initialize the video capture from the webcam.
cap = cv2.VideoCapture(0)

# We check if the webcam was opened successfully.
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# We display instructions for the user.
print("Press 'q' to quit.")

# We go through every gesture to collect the data.
for gesture in gestures:
    print(f"Perform the gesture: {gesture}")
    input("Press Enter to start collecting data...")

    while True:
        # We read a frame from the webcam.
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame from webcam.")
            break

        # We convert the image from BGR to RGB for Mediapipe processing.
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        # We check if hands have been detected in the image.
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # We extract the hand landmark coordinates and add them to the data dictionary.
                landmarks = [[lm.x, lm.y, lm.z] for lm in hand_landmarks.landmark]
                gesture_data[gesture].append(landmarks)
                # We draw the landmarks on the frame to visualize them.
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # We display the updated frame.
        cv2.imshow('Collecting Data', frame)
        # We check if the user pressed the 'q' key to stop data collection.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# We release the webcam resources and close all OpenCV windows.
cap.release()
cv2.destroyAllWindows()

# We save the collected data in a binary file 'gesture_data.pkl'.
with open('gesture_data.pkl', 'wb') as f:
    pickle.dump(gesture_data, f)

# We display a confirmation message that data collection is complete.
print("Data collection complete.")

