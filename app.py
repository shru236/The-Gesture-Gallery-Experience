import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
from gesture_detector import GestureDetectorLogger
import pickle
import os
import time

class ArtApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Art Evaluation App")  # Sets the title of the main window.

        self.root.geometry("800x600")  # Sets the dimensions of the main window.
        self.root.resizable(True, True)  # Allows window resizing.

        self.detector = GestureDetectorLogger(video_mode=True)  # Initializes the gesture detector.
        self.cap = cv2.VideoCapture(0)  # Open the webcam.

        # List of images used in the application.
        self.images = ["images/image1.jpg", "images/image2.jpg", "images/image3.jpg", "images/image4.jpg",
                       "images/image5.jpg",
                       "images/image6.jpg", "images/image7.jpg", "images/image8.jpg", "images/image9.jpg",
                       "images/image10.jpg",
                       "images/image11.jpg", "images/image12.jpg", "images/image13.jpg", "images/image14.jpg"]

        # Dictionary of image descriptions.
        self.descriptions = {
            "images/image1.jpg": "Mona Lisa - Leonardo da Vinci (1503 - 1506)",
            "images/image2.jpg": "The Starry Night - Vincent van Gogh (1889)",
            "images/image3.jpg": "Guernica - Pablo Picasso (1937)",
            "images/image4.jpg": "The Persistence of Memory - Salvador Dali (1931)",
            "images/image5.jpg": "Girl with Pearl Earring - Johannes Vermeer (1665)",
            "images/image6.jpg": "A Polish Nobleman - Rembrandt van Rijn (1637)",
            "images/image7.jpg": "Mysteries Fresco - Pompeii, Italy (middle of the 1st century BC)",
            "images/image8.jpg": "Watercolor on paper - Basawan Akbarnama (1590)",
            "images/image9.jpg": "Auspicious Cranes - Emperor Huizong of China (1112)",
            "images/image10.jpg": "The Great Wave off Kanagawa - Katsushika Hokusai (1830-1832)",
            "images/image11.jpg": " The Scream - Edvard Munch (1893)",
            "images/image12.jpg": "The Rape of the Sabine Women - Nicolas Poussin (1634-1635)",
            "images/image13.jpg": "Girls at the Gate - Nicolae Grigorescu (1885-1890)",
            "images/image14.jpg": "The Cyclops - Odilon Redon (1914)"
        }

        self.current_image_index = 0  # The index of the current image.
        self.pop_up_open = False  # Status of the pop-up window.

        self.evaluations = self.load_evaluations()  # Load ratings from file.

        # Creates a label to display the image.
        self.image_label = tk.Label(self.root)
        self.image_label.pack(expand=True, fill=tk.BOTH)

        # Creates a label for displaying the evaluation result.
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 16))
        self.result_label.pack(pady=10)

        self.last_gesture_time = 0  # The time of the last gesture detected.
        self.min_gesture_interval = 2  # Minimum interval between gestures in seconds.

        self.update_image()  # Refresh the displayed image.
        self.update_gesture()  # Update gestures.

        # Sets the action for closing the window.
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind("<Configure>", self.on_resize)  # Sets the action for resizing.

    def load_evaluations(self):
        # Load the ratings from the file if they exist, otherwise create an empty dictionary.
        if os.path.exists('evaluations.pkl'):
            with open('evaluations.pkl', 'rb') as f:
                loaded_evaluations = pickle.load(f)
                # Update keys with 'images/' prefix
                return {f'images/{k}': v for k, v in loaded_evaluations.items()}
        else:
            return {image: None for image in self.images}

    def save_evaluations(self):
        # Save ratings to file.
        # Remove the 'images/' prefix from the save.
        evaluations_to_save = {k.split('/', 1)[1]: v for k, v in self.evaluations.items()}
        with open('evaluations.pkl', 'wb') as f:
            pickle.dump(evaluations_to_save, f)

    def update_image(self):
        # Updates the displayed image based on the current index.
        image_path = self.images[self.current_image_index]
        image = Image.open(image_path)
        self.display_image(image)
        # Updates the label text with the rating of the current image.
        self.result_label.config(text=self.evaluations[self.images[self.current_image_index]] if self.evaluations[self.images[self.current_image_index]] else "")

    def display_image(self, image):
        # Gets the dimensions of the window.
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height() - 50  # Adjust the height to accommodate the label.

        if window_width <= 1 or window_height <= 1:
            window_width = 800
            window_height = 600

        # Calculates the aspect ratio of the image and the window.
        image_ratio = image.width / image.height
        window_ratio = window_width / window_height

        # Resize the image to fit in the window.
        if image_ratio > window_ratio:
            new_width = window_width
            new_height = int(window_width / image_ratio)
        else:
            new_height = window_height
            new_width = int(window_height * image_ratio)

        # If the new dimensions are valid, resize the image and update the label.
        if new_width > 0 and new_height > 0:
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            self.current_image = ImageTk.PhotoImage(resized_image)
            self.image_label.config(image=self.current_image)
            self.image_label.image = self.current_image
        else:
            print("Warning: Calculated image dimensions are zero. Skipping resize.")  # Display a warning if the calculated dimensions are zero.

    def update_gesture(self):
        # Read a frame from the webcam.
        ret, frame = self.cap.read()
        if ret:
            # Detect and record the gesture.
            gesture = self.detector.detect_and_log(frame, 0)
            self.handle_gesture(gesture)

        self.root.after(100, self.update_gesture)  # Recall this method after 100ms.

    def handle_gesture(self, gesture):
        # Handle the detected gesture.
        current_time = time.time()
        if current_time - self.last_gesture_time < self.min_gesture_interval:
            return

        self.last_gesture_time = current_time

        # Manage different gestures.
        if gesture in ["Next", "Previous"]:
            if self.pop_up_open:
                self.close_description()

            if gesture == "Next":
                self.current_image_index = (self.current_image_index + 1) % len(self.images)
            elif gesture == "Previous":
                self.current_image_index = (self.current_image_index - 1) % len(self.images)

            self.update_image()
        elif gesture == "Like":
            self.evaluations[self.images[self.current_image_index]] = "I like it."
            self.result_label.config(text="I like it.")
            self.save_evaluations()
        elif gesture == "Dislike":
            self.evaluations[self.images[self.current_image_index]] = "I don't like it."
            self.result_label.config(text="I don't like it.")
            self.save_evaluations()
        elif gesture == "Closed Palm":
            self.on_closing()
        elif gesture == "Open Palm" and not self.pop_up_open:
            self.show_description()
        elif gesture == "OK" and self.pop_up_open:
            self.close_description()
        elif gesture == "Victory":
            if self.pop_up_open:
                self.close_description()
            self.current_image_index = 0
            self.update_image()

    def show_description(self):
        # Displays the painting description in a pop-up window.
        image_path = self.images[self.current_image_index]
        description = self.descriptions[image_path]
        self.pop_up_open = True
        self.description_popup = tk.Toplevel(self.root)
        self.description_popup.title("Description of the painting")
        label = tk.Label(self.description_popup, text=description, font=("Helvetica", 14))
        label.pack(padx=20, pady=20)
        self.description_popup.protocol("WM_DELETE_WINDOW", self.close_description)

    def close_description(self):
        # Close the pop-up window.
        if self.pop_up_open:
            self.pop_up_open = False
            self.description_popup.destroy()

    def on_closing(self):
        # Save ratings and release resources before closing the app.
        self.save_evaluations()
        self.cap.release()
        self.root.destroy()

    def on_resize(self, event):
        # Refreshes the image when the window is resized.
        self.update_image()

if __name__ == "__main__":
    root = tk.Tk()  # Creates the main window.
    app = ArtApp(root)  # Create the application instance.
    root.mainloop()  # Runs the main loop of the application.
