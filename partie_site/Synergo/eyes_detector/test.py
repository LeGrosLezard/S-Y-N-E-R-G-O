import time
import cv2

import numpy as np

#Load dlib model
from recuperate_points.face_points import load_model_dlib


from recuperate_points.face_points import recuperate_landmarks
from recuperate_points.face_points import head_points
from recuperate_points.face_points import get_face_in_box
from recuperate_points.face_points import eyes_points_for_head_analysis

#Pupil part
from pupille_tracker.pupille_tracker import pupille_tracker

from paths import media_path, dlib_model




video  = media_path.format("aa.mp4")


nb_frame = 0
cap = cv2.VideoCapture(video)


predictor, detector = load_model_dlib(dlib_model)

mean_rightX = 0
mean_rightY = 0

mean_leftX = 0
mean_leftY = 0

while True:

    start_time_frame = time.time()

    _, frame = cap.read()

    height, width = frame.shape[:2]

    width_resize =  int(width / 2.9999999999999973)
    height_resize = int(height / 2.9999999999999973)
    frame = cv2.resize(frame, (width_resize, height_resize))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Recuperate landmarks and head box.
    landmarks, head_box = head_points(gray, predictor, detector) #face_points

    if landmarks is not None:

        #Recuperate pupil center, eyes constitution = (x, y), crop
        right_eye, left_eye = pupille_tracker(landmarks, frame, gray)

        print(right_eye[0], left_eye[0])

        mean_rightX
        mean_rightY

        mean_leftX
        mean_leftY


    nb_frame += 1

    cv2.imshow("Frame", frame)

    #print(time.time() - start_time_frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

 
cap.release()
cv2.destroyAllWindows()
