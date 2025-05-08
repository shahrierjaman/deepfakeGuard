# deepfake_model.py

from deepface import DeepFace
import os

def predict_deepfake(file_path, media_type):
    if media_type == 'image':
        result = DeepFace.analyze(img_path=file_path, actions=['emotion'], enforce_detection=False)
        # Here we simulate classification based on emotion detection confidence
        prediction = "Fake" if result[0]['emotion']['neutral'] < 50 else "Real"
        confidence = result[0]['emotion']['neutral']
        return prediction, confidence
    else:
        return "Unsupported", 0.0
