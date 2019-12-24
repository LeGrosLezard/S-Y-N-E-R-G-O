"""Let you watch that https://www.youtube.com/watch?v=ibuEFfpVWlU&t=518s"""

from dlib import get_frontal_face_detector, shape_predictor
import cv2
import numpy as np

from math import hypot
from scipy.spatial import distance as dist

from numpy import min as np_min
from numpy import max as np_max
from math import sin, acos, degrees





def analyse_points_for_head(landmarks):

    right_eye = landmarks.part(36).x, landmarks.part(36).y
    left_eye = landmarks.part(45).x, landmarks.part(45).y
    nose = landmarks.part(30).x, landmarks.part(30).y

    return right_eye, left_eye, nose




detector = get_frontal_face_detector()
predictor = shape_predictor("shape_predictor_68_face_landmarks.dat")







video = cv2.VideoCapture(0)





head_position = []
position = []
ok = 0
ok_haut = 0

points_position = [[], [], []]

while True:

    _, frame = video.read()
    frame, gray = resize_frame(frame)

    faces, landmarks = recuperate_landmarks(gray)

    if landmarks is not None:

        right_eye, left_eye, nose = points_for_analyse_head(landmarks)



        head = recuperate_intra_face_points(landmarks, faces, frame)
        #leaning_head(right_eye, left_eye, nose, head)
        #look_right_left(right_eye, left_eye, nose)

        moved = movements_dude(landmarks, points_position)
        if moved is True:
            points_position = [[], [], []]
        
        ok, ok_haut = look_top_bot(landmarks, frame, head_position, head, position, ok, ok_haut)
        

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


















