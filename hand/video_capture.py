import tensorflow as tf
from utils import load_inference_graph, detect_objects
import numpy as np
import cv2

print(tf.version.VERSION)



def hands_detections(scores, boxes, frame):
    """We detect hands, by position we define if it are to left or to right.
    Recup it for history if we have impossible detections"""

    width = 500; height = 400
    detections = [(int(boxes[i][1] * width), int(boxes[i][0] * height),
                   int(boxes[i][3] * width), int(boxes[i][2] * height))
                   for i in range(2) if (scores[i] > 0.10)]

    return detections


def detection_by_movement(frame, fgbg):

    background_substractor = fgbg.apply(frame)
    mask_substractor = cv2.bitwise_and(frame, frame, mask = background_substractor)

    imgray = cv2.cvtColor(mask_substractor, cv2.COLOR_BGR2GRAY)
    contours, hierarchy = cv2.findContours(imgray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    movement = [cv2.boundingRect(cnts) for cnts in contours]

##    for cnts in contours:
##        if cv2.contourArea(cnts) > 10:
##            x, y, w, h = cv2.boundingRect(cnts)
##            cv2.rectangle(frame, (x,y),(x+w, y+h), (255, 50, 25), 2)

    return movement

def detection_by_proximity(movement):
    pass



def video_capture(video_name, hand_model):

    detection_graph, sess = load_inference_graph(hand_model)

    video = cv2.VideoCapture(video_name)
    fgbg = cv2.createBackgroundSubtractorMOG2(history=120, varThreshold = 120, detectShadows=False)

    historic = []

    while True:

        

        frame = cv2.resize(video.read()[1], (500, 400))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        detections = hands_detections(scores, boxes, frame)


        for hand in detections:
            if len(hand) > 0:
                cv2.rectangle(frame, (hand[0], hand[1]), (hand[2], hand[3]), (79, 220, 25), 4)
            else:
                print("processus de recherche")
                detection_by_movement(frame, fgbg)

        historic = [ [int(hand[0] + hand[2] / 2), int(hand[1] + hand[3] / 2)] for hand in detections]

    



        cv2.imshow("frame", frame)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

        frame += 1

    video.release()
    cv2.destroyAllWindows()





















