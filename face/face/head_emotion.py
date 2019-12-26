"""Here analysis"""
import cv2
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import img_to_array

def load_model_emotion(emotion_model):
    emotion_classifier = load_model(emotion_model, compile=False)
    return emotion_classifier


def head_emotion(head_box, emotion_classifier, gray):


    EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]

    (x, y, w, h) = head_box
    roi = gray[y:y + h, x:x + w]
    roi = cv2.resize(roi, (64, 64))
    roi = roi.astype("float") / 255.0
    roi = img_to_array(roi)
    roi = np.expand_dims(roi, axis=0)
    preds = emotion_classifier.predict(roi)[0]
    emotion_probability = np.max(preds)
    label = EMOTIONS[preds.argmax()]

    return label
    #putText(frame, label, (fX, fY - 10), FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
    #rectangle(frame, (fX, fY), (fX + fW, fY + fH),(0, 0, 255), 2)
