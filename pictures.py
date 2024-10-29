# We import the GestureDetector Logger class from the gesturedetector module.
from gesture_detector import GestureDetectorLogger
# We import the ArtApp class from the app module.
from app import ArtApp
# We import the tkinter module to create the GUI.
import tkinter as tk

# The main function to run the application.
def run_app():
    # We create an instance of the main Tkinter window.
    root = tk.Tk()
    # We create an instance of ArtApp, which takes the main window as a parameter.
    app = ArtApp(root)
    # We start the Tkinter main loop, which waits for and handles UI events.
    root.mainloop()

# If the file is run directly (not imported as a module), we call the run_app function to start the application.
if __name__ == "__main__":
    run_app()
