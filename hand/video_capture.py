import cv2
import tensorflow as tf
import numpy as np
from time import time
import imutils
from utils import load_inference_graph, detect_objects

print(tf.version.VERSION)



def subastractor_background(frame, movement_mask, fgbg):
    suba = fgbg.apply(frame)
    contours, _ = cv2.findContours(suba, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    for cnts in contours:
        if 1000 > cv2.contourArea(cnts) > 250: #ICI RATIO:
            x, y, w, h = cv2.boundingRect(cnts)
            movement_mask.append((x, y, x+w, y+h))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3, 1)

def hands_detections(scores, boxes, right, history_right, left, hitstory_left, frame):
    for i in range(2):
        if (scores[i] > 0.10):
            (x, x1, y, y1) = (boxes[i][1] * 500, boxes[i][3] * 500, boxes[i][0] * 400, boxes[i][2] * 400)

            cv2.rectangle(frame, (x, y), (x1, y1), (0, 0, 0), 3, 1)

            if p1[0] < 250:
                right.append((x, y, x1, y1))
                history_right[0].append(x)
                history_right[1].append(y)
            else:
                left.append((x, y, x1, y1))
                hitstory_left[0].append(x)
                hitstory_left[1].append(y)


def detection_possible(historic, possibility, movement):

    possibility = "possible"
    if abs(historic[0][-1] - historic[0][-2]) > 50 or\
       abs(historic[1][-1] - historic[1][-2]) > 50:
        possibility = "impossible"
        if possibility == "impossible":
            movement.remove(droite[-1])
            historic[0].remove(historic[-1])
            historic[1].remove(historic[-1])

    return possibility


def substractor_hand_movement(movement_mask, movement):
    nb = 80
    points = [[], [], [], []]

    for i in movement_mask:
        if abs(i[0] - movement[0][0]) < nb and\
           abs(i[1] - movement[0][1]) < nb and\
           abs(i[1] - movement[0][1]) < nb and\
           abs(i[3] - movement[0][3]) < nb:
            points[0].append(i[0])
            points[1].append(i[1])
            points[2].append(i[2])
            points[3].append(i[3])

    return points




def requalibrage_movement(frame, points, movement, historic, possibility):

    #Draw detection
    if len(points[0]) != 0:
        cv2.rectangle(frame, (min(points[0]), min(points[1])), (max(points[2]), max(points[3])), (77, 0, 0), 3, 1)

    #No detection
    if len(movement) == 1 and and len(points[0]) != 0:
        movement.append( ( min(points[0]), min(points[1]), max(points[2]), max(points[3]) ) )

        historic[0].append(min(points[0]))
        historic[1].append(min(points[1]))

    #Fusion of detections

    elif len(movement) == 2 and len(points[0]) != 0:
        fusion_points = [[], [], [], []]

        for i in range(4):
            fusion_points[i].append(movement[-1][i])

        for nb, i in enumerate(points):
            for j in i:
                fusion_points[nb].append(j)

        movement[-1] = (min(fusion_points[0]), min(fusion_points[1]), max(fusion_points[2]), max(fusion_points[3]))


    #Impossible detection
    if possibility == "impossible" and len(points[0]) != 0:
        movement[-1] = ((min(points[0]), min(points[1]), max(points[2]), max(points[3])))

    if len(movement) == 3:
        a = movement[0][0] - movement[1][0]
        b = movement[0][0] -  movement[2][0]
        if a < b:
            movement[-1] = movement[-2]

    return movement, historic


def video_capture(video_name, hand_model):

    detection_graph, sess = load_inference_graph(hand_model)
    video = cv2.VideoCapture(video_name)

    fgbg = cv2.createBackgroundSubtractorMOG2(history=10, detectShadows=False)



    history_right = [[], []]
    right = []
    hitstory_left = [[], []]
    left = []

    while True:

        movement_mask = []
        right_possibility = ""
        left_possibility = ""



        frame = cv2.resize(video.read()[1], (500, 400))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        #Make a substraction of the background and recup movements.
        subastractor_background(frame, movement_mask, fgbg)


        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        hands_detections(scores, boxes, right, history_right, left, hitstory_left, frame):
        try:
            print(hist_droite[0][-1], (hist_droite[0][-2]))
            print(hist_gauche[0][-1], (hist_gauche[0][-2]))

            right_pos = detection_possible(history_right, right_possibility, right)
            left_pos = detection_possible(hitstory_left, left_possibility, left)

            right_points = substractor_hand_movement(movement_mask, right)
            left_points = substractor_hand_movement(movement_mask, left)

            right, history_right = requalibrage_movement(frame, right_points, right, history_right, right_possibility)
            left, hitstory_left = requalibrage_movement(frame, left_points, left, hitstory_left, left_possibility)

        except:pass


            cv2.rectangle(frame, (right[-1][0], right[-1][1]), (right[-1][2], right[-1][3]), (77, 255, 9), 1)
            cv2.rectangle(frame, (left[-1][0], left[-1][1]), (left[-1][2], left[-1][3]), (77, 255, 9), 1)


            print("droite", right)
            print("gauche", left)


            right = [right[-1]]
            left = [left[-1]]
        
    
        except:
            pass

        cv2.imshow("mask", frame)


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
