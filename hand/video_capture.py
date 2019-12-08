import cv2
import tensorflow as tf
import numpy as np
from time import time
import imutils
from utils import load_inference_graph, detect_objects


print(tf.version.VERSION)


def sustractor_background(frame, fgbg, liste):

    R = cv2.RETR_TREE
    P = cv2.CHAIN_APPROX_NONE
    suba = fgbg.apply(frame)
    contours, _ = cv2.findContours(suba, R, P)
    for cnts in contours:
        if 1000 > cv2.contourArea(cnts) > 250: #500 / 1.7:
            x, y, w, h = cv2.boundingRect(cnts)
            liste.append((x, y, x+w, y+h))
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3, 1)

def hands_detections(scores, boxes, droite, gauche, hist_droite, hist_gauche, frame):

    for i in range(2):
        if (scores[i] > 0.10):
            (left, right, top, bottom) = (boxes[i][1] * 500, boxes[i][3] * 500,
                                          boxes[i][0] * 400, boxes[i][2] * 400)
            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))

            cv2.rectangle(frame, p1, p2, (255, 255, 200), 1)


            if p1[0] < 250:
                droite.append((p1[0], p1[1], p2[0], p2[1]))
                hist_droite[0].append(p1[0])
                hist_droite[1].append(p1[1])
            else:
                gauche.append((p1[0], p1[1], p2[0], p2[1]))
                hist_gauche[0].append(p1[0])
                hist_gauche[1].append(p1[1])


def possibles_movement(historic, movement):

    if abs(historic[0][-1] - historic[0][-2]) > 50 or\
       abs(historic[1][-1] - historic[1][-2]) > 50:
        possibility = "impossible"

        if possibility == "impossible":
            movement.remove(movement[-1])
        


def detections_from_substractor(points_movements, movement):
    points = [[], [], [], []]; nb = 80

    for i in points_movements:
        a = abs(i[0] - movement[0][0])
        b = abs(i[1] - movement[0][1])
        c = abs(i[2] - movement[0][2])
        d = abs(i[3] - movement[0][3])

        if a < nb and b < nb and c < nb and d < nb:
            points[0].append(i[0])
            points[1].append(i[1])
            points[2].append(i[2])
            points[3].append(i[3])
                   
    return points



def draw(frame, points_movements):
    if len(points_movements[0]) != 0:
        cv2.rectangle(frame, (min(points_movements[0]), min(points_movements[1])),
                             (max(points_movements[2]), max(points_movements[3])),
                      (77, 0, 0), 3, 1)


def no_hand_detection(movement, points_movements, historic):

    if len(movement) == 1 and len(points_movements[0]) != 0:

        movement.append((min(points_movements[0]), min(points_movements[1]),
                         max(points_movements[2]), max(points_movements[3])))

        historic[0].append(min(points_movements[0]))
        historic[1].append(min(points_movements[1]))

def fusion_movement_detection(movement, points_movements):
    
    if len(movement) == 2 and len(points_movements[0]) != 0:
        fusion = [[], [], [], []]

        for i in range(4):
            fusion[i].append(movement[-1][i])

        for nb, i in enumerate(points_movements):
            for j in i:
                fusion[nb].append(j)

        movement[-1] = (min(fusion[0]), min(fusion[1]), max(fusion[2]), max(fusion[3]))

def false_hand_detection(possibility, points_movements, movement):

    if possibility == "impossible" and len(points_movements[0]) != 0:
        movement[-1] = ((min(points_movements[0]), min(points_movements[1]),
                       max(points_movements[2]), max(points_movements[3])))


def more_than_one_detection(movement):

    if len(movement) == 3:
        a = movement[0][0] - movement[1][0]
        b = movement[0][0] -  movement[2][0]
        if a < b:
            movement[-1] = droite[-2]



def video_capture(video_name, hand_model):

    detection_graph, sess = load_inference_graph(hand_model)
    video = cv2.VideoCapture(video_name)
    detections = [[], []]
    fgbg = cv2.createBackgroundSubtractorMOG2(history=10, detectShadows=False)

    droite = []
    gauche = []

    hist_droite = [[], []]
    hist_gauche = [[], []]
    while True:

        points_movements = []
        possible_droite = "possible"
        possible_gauche = "possible"


        frame = cv2.resize(video.read()[1], (500, 400))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        sustractor_background(frame, fgbg, points_movements)



        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        hands_detections(scores, boxes, droite, gauche, hist_droite, hist_gauche, frame)


        if len(hist_droite[0]) >= 2:
            possibles_movement(hist_droite, droite)
            possibles_movement(hist_gauche, gauche)

            print("droite", possible_droite)
            print("gauche", possible_gauche)


        droite_points = detections_from_substractor(points_movements, droite)
        gauche_points = detections_from_substractor(points_movements, gauche)

        draw(frame, droite_points)
        draw(frame, gauche_points)

        no_hand_detection(droite, droite_points, hist_droite)
        no_hand_detection(gauche, gauche_points, hist_gauche)

        fusion_movement_detection(droite, droite_points)
        fusion_movement_detection(gauche, gauche_points)


        false_hand_detection(possible_droite, droite_points, droite)
        false_hand_detection(possible_gauche, gauche_points, gauche)

        more_than_one_detection(droite)
        more_than_one_detection(gauche)



        cv2.rectangle(frame, (droite[-1][0], droite[-1][1]),
                      (droite[-1][2], droite[-1][3]), (77, 255, 9), 3)

        cv2.rectangle(frame, (gauche[-1][0], gauche[-1][1]),
                      (gauche[-1][2], gauche[-1][3]), (77, 255, 9), 3)


        droite = [droite[-1]]
        gauche = [gauche[-1]]
        











        cv2.imshow("mask", frame)


        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
