import time

start_time_import = time.time()

import cv2
import numpy as np

from face_points import recuperate_landmarks
from face_points import head_points
from face_points import get_face_in_box
from face_points import eyes_points_for_head_analysis


#Blink part
from blinking_eyes import blinking_eyes
from analysis_eyes import blink_analysis

#Pupil part
from pupille_tracker import pupille_tracker

#Eyes movement part
from eyes_movement import eyes_movements

#Path to model, to media folder.
from paths import media_path, dlib_model

#Load dlib model
from face_points import load_model_dlib

#Resize video.
from pre_test import search_video_size

print("Import time : ", time.time() - start_time_import)




video  = media_path.format("a.mp4")
predictor, detector = load_model_dlib(dlib_model)

video_size = search_video_size(video, predictor, detector, dlib_model)


nb_frame = 0
cap = cv2.VideoCapture(video)

while True:

    _, frame = cap.read()

    height, width = frame.shape[:2]

    width  = int(width  /  video_size)
    height = int(height /  video_size)


    frame = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
##
##    #Recuperate landmarks and head box.
##    landmarks, head_box = head_points(gray, predictor, detector)


#    if landmarks is not None:

        #Recuperate blink algorythme
#        blinking_frame, result = blinking_eyes(landmarks, head_box)
##        blink_analysis(result, nb_frame, blinking_frame)
##
##        #Recuperate pupil center
##        right_eye, left_eye = pupille_tracker(landmarks, frame, gray)
##        eyes = eyes_movements(landmarks, frame, right_eye, left_eye)



    nb_frame += 1
    cv2.imshow("Frame", frame)


    
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
