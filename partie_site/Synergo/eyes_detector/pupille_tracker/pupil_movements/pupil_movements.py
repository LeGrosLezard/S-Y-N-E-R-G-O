import cv2
import numpy as np
from scipy.spatial import distance as dist

from ..head_movements.turn_head import turn_head
from ..head_movements.bent_up_head import bent_up_head


def face_movement(landmarks, frame, eyes, head_box):


    eyeR_pts = landmarks.part(36).x, landmarks.part(36).y
    eyeL_pts = landmarks.part(45).x, landmarks.part(45).y
    noze_pts = landmarks.part(30).x, landmarks.part(30).y

    out = None
    out1 = None

    turning = turn_head(eyeR_pts, eyeL_pts, noze_pts, head_box)
    #print(turning)

    head_position = bent_up_head(eyeR_pts, eyeL_pts, noze_pts, head_box)
    #print("head position : ", head_position)

    if turning == "legerement a gauche":
        out = "gauche"
    elif turning == "legerement a droite":
        out =  "droite"

    if head_position == "position baissé":
        out1 = "bas"
    elif head_position == "position levé":
        out1 = "haut"

    return out, out1





TIMMER = []
POSITION_RIGHT = []
POSITION_LEFT = []

def recuperate_pupil_center(extremum, frame):

    #Recuperate left, right, top, bot corner of the eye
    xExtremum, yExtremum, wExtremum, hExtremum = extremum

    #Search our red mark who's center of the eye.
    center_pupil = [(j, i) for i in range(yExtremum[1], hExtremum[1])
           for j in range(xExtremum[0], wExtremum[0])
           if frame[i, j][0] == 0 and frame[i, j][1] == 0 and frame[i, j][2] == 255]

    return center_pupil


def x_movements(blanck, frame, glob, center_pupil, eyes):

    global COEF_X

    cv2.circle(blanck, center_pupil[0], 1, (0, 255, 0), 1)
    cv2.circle(frame, center_pupil[0], glob, (0, 255, 0), 1)

    right_point = tuple(eyes[0][3][0])
    left_point  = tuple(eyes[0][0][0])

    #Recuperate width on x axis distance from the eye.
    total = int(dist.euclidean( (right_point[0], 0), (left_point[0], 0) ))

    #Center X of the eye in comparaison of right side.
    right_distance = dist.euclidean( (eyes[0][3][0][0], 0), (center_pupil[0][0], 0) )
    #Center X of the eye in comparaison of left side.
    left_distance = dist.euclidean( (eyes[0][0][0][0], 0),  (center_pupil[0][0], 0) )

    #print(total, left_distance, right_distance)
    if left_distance <= int(total * COEF_X):
        print("oeil gauche")
    elif right_distance <= int(total * COEF_X):
        print("oeil droite") 


def y_movements(landmarks, head_box, center_pupil, glob):

    global COEF_Y_COMPARAISON_MID_TOP  #coef mid eye/top eye.
    global COEF_Y_COMPARAISON_GLOB_TOP #coef glob/top eye.

    global COEF_Y_COMPARAISON_MID_BOT  #coef mid eye/bot eye.
    global COEF_Y_COMPARAISON_GLOB_BOT #coef glob eye/bot eye.

    """MIDDLE OF THE EYE (mean y axis)"""
    #Extremums landmarks points from dlib.
    right_point_eye = landmarks.part(36).x, landmarks.part(36).y
    left_point_eye  = landmarks.part(39).x, landmarks.part(39).y
    #Recuperate mean of the height midle of the eye.
    middle_mean_height = int( (right_point_eye[1] + left_point_eye[1]) / 2)

    """POSITION PUPIL/MIDDLE OF THE EYE"""
    #Recuperate height distance beetween the center and the pupil.
    mid_top = dist.euclidean((0, middle_mean_height), (0, center_pupil[0][1]))

    """BOTTOM Y POSITION (mean)"""
    #Recuperate the mean of the bottom of the points of the eye.
    bottom_eye_1 = landmarks.part(41).x, landmarks.part(41).y
    bottom_eye_2 = landmarks.part(40).x, landmarks.part(40).y
    middle_mean_height = int( (bottom_eye_1[1] + bottom_eye_2[1]) / 2)

    """TOP Y POSITION (mean)"""
    #Recuperate the mean of the top of the points of the eye.
    top_eye_1 = landmarks.part(37).x, landmarks.part(37).y
    top_eye_2 = landmarks.part(38).x, landmarks.part(38).y
    mean_of_the_bottom = int( (top_eye_1[1] + top_eye_2[1]) / 2)

    """DISTANCE TOP/BOT EYE (mean)"""
    #Recuperate distance beetween top and bottom means points.
    height = dist.euclidean( (0, middle_mean_height), (0, mean_of_the_bottom) )

    
    if mid_top >= int(height * COEF_Y_COMPARAISON_MID_TOP) and\       #mid in comparaison height.
       height >= int(head_box[3] * COEF_Y_COMPARAISON_GLOB_TOP):      #glob in comparaison height.
        print("haut")

    elif height <= int(head_box[3] *  COEF_Y_COMPARAISON_MID_BOT) and\ #height in comparaison height head.
         glob <= int(height * COEF_Y_COMPARAISON_GLOB_BOT):            #glob in comparaison height head.
        print("bas")


COEF_X = 0.42                       #coef x axis.
COEF_Y_COMPARAISON_MID_TOP = 0.34   #coef mid eye/top eye.
COEF_Y_COMPARAISON_GLOB_TOP = 0.065 #coef glob eye/top eye.

COEF_Y_COMPARAISON_MID_BOT = 0.036  #coef mid eye/bot eye.
COEF_Y_COMPARAISON_GLOB_BOT = 0.5   #coef glob eye/bot eye.



def eyes_movements(informations):

    global COEF_X                       #coef x axis.
    global COEF_Y_COMPARAISON_MID_TOP   #coef mid eye/top eye.
    global COEF_Y_COMPARAISON_GLOB_TOP  #coef glob eye/top eye.

    global COEF_Y_COMPARAISON_MID_BOT   #coef mid eye/bot eye.
    global COEF_Y_COMPARAISON_GLOB_BOT  #coef glob eye/bot eye.

    #frame, extremums of eyes, eyes landmarks, eye right or left.
    frame, extremum, landmarks, head_box, eyes, glob, blanck, the_eye = informations

    if the_eye == "right":

        #Recuperate center of the pupil.
        center_pupil = recuperate_pupil_center(extremum, frame)

        #Pupil regulation.
        if center_pupil != []:

            #X movements.
            x_movements(blanck, frame, glob, center_pupil, eyes)
            #Y movmeents.
            y_movements(landmarks, head_box, center_pupil, glob)




    if the_eye == "left":
        center_pupil = recuperate_pupil_center(extremum, frame)

        if center_pupil != []:

            cv2.circle(blanck, center_pupil[0], 1, (0, 255, 0), 1)
            cv2.circle(frame, center_pupil[0], glob, (0, 0, 255), 1)


            left_point = tuple(eyes[1][3][0])
            right_point  = tuple(eyes[1][0][0])

            total = int(dist.euclidean( (right_point[0], 0), (left_point[0], 0) ))

            left_distance = dist.euclidean( (right_point[0], 0), (center_pupil[0][0], 0) )
            right_distance = dist.euclidean( (left_point[0], 0),  (center_pupil[0][0], 0) )

            if left_distance <= int(total * COEF_X):
                print("oeil gauche")
            elif right_distance <= int(total * COEF_X):
                print("oeil droite")



            right_point_eye = landmarks.part(42).x, landmarks.part(42).y
            left_point_eye = landmarks.part(45).x, landmarks.part(45).y

            middle_mean_height = int((right_point_eye[1] + left_point_eye[1])/2)

            mid_top = dist.euclidean((0, middle_mean_height), (0, center_pupil[0][1]))

            bottom_eye_1 = landmarks.part(47).x, landmarks.part(47).y
            bottom_eye_2 = landmarks.part(46).x, landmarks.part(46).y
            middle_mean_height = int((bottom_eye_1[1] + bottom_eye_2[1])/2)

            top_eye_1 = landmarks.part(43).x, landmarks.part(43).y
            top_eye_2 = landmarks.part(44).x, landmarks.part(44).y
            mean_of_the_bottom = int((top_eye_1[1] + top_eye_2[1])/2)


            height = dist.euclidean( (0, middle_mean_height), (0, mean_of_the_bottom) )


            if mid_top >= int(height * 0.34) and height >= int(head_box[3] * 0.065):
                print("haut")

            elif height <= int(head_box[3] *  0.036) and glob <= int(height * 0.5):
                print("bas")


