import threading
import numpy as np
import cv2
from roop.typing import Frame

PREDICTOR = None
THREAD_LOCK = threading.Lock()
MAX_PROBABILITY = 0.85


def get_predictor() -> None:
    # This function is not needed as we are not using a pre-trained model
    pass


def clear_predictor() -> None:
    # This function is not needed as we are not using a pre-trained model
    pass


def predict_frame(target_frame: Frame) -> bool:
    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(target_frame, cv2.COLOR_BGR2GRAY)
    # Use a simple thresholding technique to detect NSFW content
    _, thresholded_frame = cv2.threshold(gray_frame, 127, 255, cv2.THRESH_BINARY)
    # Calculate the percentage of white pixels in the frame
    white_pixel_percentage = np.sum(thresholded_frame == 255) / target_frame.size
    return white_pixel_percentage > MAX_PROBABILITY


def predict_image(target_path: str) -> bool:
    # Load the image
    image = cv2.imread(target_path)
    if image is None:
        raise ValueError("Unable to load the image.")
    # Predict NSFW content in the image
    return predict_frame(image)


def predict_video(target_path: str) -> bool:
    # Initialize the video capture object
    cap = cv2.VideoCapture(target_path)
    if not cap.isOpened():
        raise ValueError("Unable to open the video file.")
    # Read frames from the video and predict NSFW content
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        if predict_frame(frame):
            return True
    # Release the video capture object
    cap.release()
    return False
