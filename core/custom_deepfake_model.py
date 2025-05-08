import tensorflow as tf
import cv2
import numpy as np
import os

# Load the trained model
model_path = os.path.join(os.path.dirname(__file__), '../training/deepfake_detector.h5')
model = tf.keras.models.load_model(model_path)

def predict_deepfake(file_path, media_type):
    try:
        img_size = (224, 224)
        if media_type == 'image':
            # Check file extension to determine how to load
            if file_path.endswith('.png'):
                img = cv2.imread(file_path)
                if img is None:
                    return 'Pending', 0.0
                img = cv2.resize(img, img_size)
                img = img / 255.0
                img = np.expand_dims(img, axis=0)
                confidence = model.predict(img)[0][0] * 100
                prediction = 'Potential Deepfake' if confidence > 50 else 'Authentic'
                return prediction, confidence
            elif file_path.endswith('.npy'):
                try:
                    data = np.load(file_path)
                    if len(data.shape) == 3 and data.shape[2] in [1, 3]:  # Image-like data
                        img = cv2.resize(data, img_size)
                        if img.shape[2] == 1:
                            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
                        img = img / 255.0
                        img = np.expand_dims(img, axis=0)
                        confidence = model.predict(img)[0][0] * 100
                        prediction = 'Potential Deepfake' if confidence > 50 else 'Authentic'
                        return prediction, confidence
                    else:
                        return 'Pending', 0.0
                except Exception as e:
                    print(f"[ERROR] Failed to process .npy file {file_path}: {str(e)}")
                    return 'Pending', 0.0
            else:
                return 'Pending', 0.0

        elif media_type == 'video':
            cap = cv2.VideoCapture(file_path)
            frames = []
            while len(frames) < 1 and cap.isOpened():  # Extract 1 frame
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(cv2.resize(frame, img_size) / 255.0)
            cap.release()

            if not frames:
                return 'Pending', 0.0

            predictions = []
            for frame in frames:
                frame = np.expand_dims(frame, axis=0)
                pred = model.predict(frame)[0][0]
                predictions.append(pred)

            confidence = np.mean(predictions) * 100
            prediction = 'Potential Deepfake' if confidence > 50 else 'Authentic'
            return prediction, confidence

        else:
            return 'Pending', 0.0

    except Exception as e:
        print(f"[ERROR] Deepfake analysis failed: {str(e)}")
        return 'Pending', 0.0