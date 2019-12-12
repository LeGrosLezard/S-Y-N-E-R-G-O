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

    gray = cv2.cvtColor(mask_substractor, cv2.COLOR_BGR2GRAY)
    contours = cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0]

    movement = [cv2.boundingRect(cnts) for cnts in contours]

    return movement



def detection_by_proximity(movement, historic):

    out = [[], []]

    def define_movement(movement, historic, nb):

        return [move for move in movement if abs(move[0] - historic[nb][0]) < 40 and\
                                             abs(move[1] - historic[nb][1]) < 40]

    if len(historic) > 0:

        if len(historic[0]) > 0:
            out[0] = define_movement(movement, historic, 0)

        if len(historic[1]) > 0:
            out[1] = define_movement(movement, historic, 1)

    return out[0], out[1]



def make_movement_detection(hand_movement_right, hand_movement_left, frame, historic):


    out = [[], []]

    def define_points(movement):

        liste = [[], [], [], []]
        for i in movement:
            liste[0].append(i[0])
            liste[1].append(i[1])
            liste[2].append(i[0] + i[2])
            liste[3].append(i[1] + i[3])

        return  min(liste[0]), min(liste[1]), max(liste[2]), max(liste[3])

    if hand_movement_right != []:
        out[0] = define_points(hand_movement_right)

    if hand_movement_left != []:
        out[1] = define_points(hand_movement_left)


    return out


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


        movements = detection_by_movement(frame, fgbg)
        hand_movement_right, hand_movement_left = detection_by_proximity(movements, historic)
        right_detection, left_detection = make_movement_detection(hand_movement_right, hand_movement_left, frame, historic)

        if right_detection != []:
            cv2.rectangle(frame, (right_detection[0], right_detection[1]),
                          (right_detection[2], right_detection[3]), (100, 50, 255), 3)

        if left_detection != []:
            cv2.rectangle(frame, (left_detection[0], left_detection[1]),
                          (left_detection[2], left_detection[3]), (100, 50, 255), 3)

        historic = [ [int((hand[0] + hand[2]) / 2), int((hand[1]+hand[3]) / 2)] for hand in detections]

    








        cv2.imshow("frame", frame)
        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

        frame += 1

    video.release()
    cv2.destroyAllWindows()





















