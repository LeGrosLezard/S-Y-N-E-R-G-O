import cv2
import tensorflow as tf
import numpy as np
from time import time
import imutils
from utils import load_inference_graph, detect_objects


print(tf.version.VERSION)


def hands_detections(scores, boxes, droite, gauche, hist_droite, hist_gauche, frame):
    """We detect hands, by position we define if it are to left or to right.
    Recup it for history if we have impossible detections"""

    for i in range(2):
        if (scores[i] > 0.10):
            (left, right, top, bottom) = (boxes[i][1] * 500, boxes[i][3] * 500,
                                          boxes[i][0] * 400, boxes[i][2] * 400)
            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))
            cv2.rectangle(frame, p1, p2, (0, 0, 0), 4)

    detected_points = [(int(boxes[i][1] * 500), int(boxes[i][3] * 500),
                        int(boxes[i][0] * 400), int(boxes[i][2] * 400)) for i in range(2) if scores[i] > 0.10]

    right_left_points = [  [(pt[0], pt[2], pt[1], pt[3]) for pt in detected_points if pt[0] < 250],
                           [(pt[0], pt[2], pt[1], pt[3]) for pt in detected_points if pt[0] > 250]   ]


def video_capture(video_name, hand_model):

    detection_graph, sess = load_inference_graph(hand_model)
    video = cv2.VideoCapture(video_name)
    fgbg = cv2.createBackgroundSubtractorMOG2(history=120, detectShadows=False)

    droite = []; gauche = []; hist_droite = [[], []]; hist_gauche = [[], []]

    while True:





        frame = cv2.resize(video.read()[1], (500, 400))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        hands_detections(scores, boxes, droite, gauche, hist_droite, hist_gauche, frame)





        cv2.imshow("mask", frame)


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
