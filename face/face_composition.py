import cv2
import numpy as np


def make_landmarks_points(landmarks, area):
    return np.array([(landmarks.part(n).x, landmarks.part(n).y)
                     for n in range(area[0], area[1])])

def on_eyes(landmarks, frame):
    on_eyes_points = {"onEye1":[18, 22], "onEye2":[22, 26]}


    onEye1 = make_landmarks_points(landmarks, on_eyes_points["onEye1"])
    onEye2 = make_landmarks_points(landmarks, on_eyes_points["onEye2"])  


    for i in onEye1:
        cv2.circle(frame, (i[0], i[1]), 1, (0, 255, 0), 1)

    for i in onEye2:
        cv2.circle(frame, (i[0], i[1]), 1, (0, 255, 0), 1)







    #monté 2
    #monté 1
    #baisse vers l'intérieur 1
    #baisse vers l'intérieur 2









