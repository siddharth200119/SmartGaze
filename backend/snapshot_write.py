import os
import cv2
from datetime import datetime

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d_%H-%M-%S")

def take_snapshot(camera_index=0, directory='C:/Users/mohit/Desktop/photos', filename=None):
    if filename is None:
        filename = f"{get_current_datetime()}.jpg"

    filepath = os.path.join(directory, filename)

    camera = cv2.VideoCapture(camera_index)

    if not camera.isOpened():
        print("Error: Could not open camera.")
        return

    ret, frame = camera.read()

    if ret:
        cv2.imwrite(filepath, frame)
        print(f"Snapshot saved as {filepath}")
    else:
        print("Error: Could not capture snapshot.")

    camera.release()

take_snapshot(directory='C:/Users/mohit/Desktop/photos')

 
