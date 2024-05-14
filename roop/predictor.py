import opennsfw2
from PIL import Image
from roop.typing import Frame

PREDICTOR = None

def get_predictor() -> opennsfw2.Model:
    global PREDICTOR
    if PREDICTOR is None:
        PREDICTOR = opennsfw2.make_open_nsfw_model()
    return PREDICTOR

def predict_frame(target_frame: Frame) -> float:
    image = Image.fromarray(target_frame)
    image = opennsfw2.preprocess_image(image, opennsfw2.Preprocessing.YAHOO)
    views = numpy.expand_dims(image, axis=0)
    return get_predictor().predict(views)[0][1]  # Return the probability directly

def predict_image(target_path: str) -> float:
    return opennsfw2.predict_image(target_path)  # Return the probability directly

def predict_video(target_path: str) -> list[float]:
    _, probabilities = opennsfw2.predict_video_frames(video_path=target_path, frame_interval=100)
    return probabilities  # Return a list of probabilities for each frame
