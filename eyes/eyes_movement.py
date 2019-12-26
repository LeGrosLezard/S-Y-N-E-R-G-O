import cv2
import numpy as np


LAST_H_RIGHT = []
LAST_H_LEFT = []
def eyes_position(landmarks, frame, right_eye, left_eye):

    global LAST_H_RIGHT
    global LAST_H_LEFT

    eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
            for n in range(36, 42)])),
    cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
            for n in range(42, 48)])))

    right = ""
    left = ""
    right_top = ""
    left_top = ""
    right_bot = ""
    left_bot = ""
    if right_eye[0] is not None:

        x, y, w, h = cv2.boundingRect(eyes[0])
        cv2.rectangle(frame, (x, (y-5)), (x+w, y+h+5), (0,255,0), 1)

        x_center = right_eye[0]
        y_center = right_eye[1]

        h = h + 10



        if len(LAST_H_RIGHT) >= 2 and h >= LAST_H_RIGHT[-2] + 2 and y_center >= int(0.40*h):
            right_top = "haut"
        else:
            LAST_H_RIGHT.append(h)

        #if height of detection shrink of -1.5 of the mean height frame
        #and pupil Y < 40% of the height of frame
        if h <=  np.mean(LAST_H_RIGHT) - 1.5 and y_center <= int(0.45*h):
            right_bot = "bas"

            if x_center >= int(0.80 * w):
                right = "bas gauche"

            elif x_center <= int(0.65 * w):
                right = "bas droite"


        if x_center >= int(0.85 * w):
            right = "gauche"

        elif x_center <= int(0.72 * w):
            right = "droite"










    if left_eye[0] is not None:

        x, y, w, h = cv2.boundingRect(eyes[1])
        cv2.rectangle(frame, (x, (y-5)), (x+w, y+h+5), (0,255,0), 1)

        x_center = left_eye[0]
        y_center = left_eye[1]

        h = h + 10


        if len(LAST_H_LEFT) >= 2 and h >= LAST_H_LEFT[-2] + 2 and y_center >= int(0.40*h):
            left_top = "haut"
        else:
            LAST_H_LEFT.append(h)

        #if height of detection shrink of -1.5 of the mean height frame
        #and pupil Y < 40% of the height of frame
        if h <=  np.mean(LAST_H_LEFT) - 1.5 and y_center <= int(0.45*h):
            left_bot = "bas"

            if x_center >= int(0.80 * w):
                left = "bas gauche"

            elif x_center <= int(0.65 * w):
                left = "bas droite"


        if x_center >= int(0.85 * w):
            left = "gauche"

        elif x_center <= int(0.72 * w):
            left = "droite"



    movement = ""

    if right == "gauche" and left == "gauche":
        movement += "gauche "
    elif right == "droite" and left == "droite":
        movement += "droite "


    if right_top == "haut" and left_top == "haut":
        movement += "haut "
    elif right_bot == "bas" and left_bot == "bas":
        movement += "bas "

    if right == "bas gauche" and left == "bas gauche":
        movement += "bas gauche "
    elif right == "bas droite" and left == "bas droite":
        movement += "bas droite "




    if movement != "":
        print(movement)







        



