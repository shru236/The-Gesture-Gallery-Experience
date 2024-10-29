# We import the necessary modules for data manipulation and machine learning model creation.
import pickle
import numpy as np
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# We open the 'gesture_data.pkl' file in binary read mode and load the gesture data.
with open('gesture_data.pkl', 'rb') as f:
    gesture_data = pickle.load(f)

# We initialize the lists for the features (X) and labels (y) of the gestures.
X = []
y = []

# We walk through each gesture and its set of landmarks.
for gesture, landmarks in gesture_data.items():
    # For each set of landmark points, we flatten the array into a vector and add it to X.
    for landmark in landmarks:
        X.append(np.array(landmark).flatten())
        # We add the label corresponding to the gesture in y.
        y.append(gesture)

# We convert the x and y lists to NumPy arrays to facilitate further processing.
X = np.array(X)
y = np.array(y)

# We create a pipeline that includes standard data scaling and linear kernel SVM model.
model = make_pipeline(StandardScaler(), SVC(kernel='linear', probability=True))

# We train the model on the training data (X and y).
model.fit(X, y)

# We save the trained model in a binary file 'gesture_model.pkl'.
with open('gesture_model.pkl', 'wb') as f:
    pickle.dump(model, f)


# We display a confirmation message that the model training is complete.
print("Model training complete.")
