import time

start_time_import = time.time()

import cv2
import numpy as np

from recuperate_points.face_points import recuperate_landmarks
from recuperate_points.face_points import head_points
from recuperate_points.face_points import get_face_in_box
from recuperate_points.face_points import eyes_points_for_head_analysis


#Blink part
from blinking.blinking_eyes import blinking_eyes
from blinking.blinking_eyes import blink_analysis

#Pupil part
from pupille_tracker.pupille_tracker import pupille_tracker

#Eyes movement part
from eyes_movement.eyes_movement import eyes_movements, eyes_contours

#Path to model, to media folder.
from paths import media_path, dlib_model

#Load dlib model
from recuperate_points.face_points import load_model_dlib

#Resize video.
from pre_test import search_video_size

print("Import time : ", time.time() - start_time_import)




video  = media_path.format("a.mp4")
predictor, detector = load_model_dlib(dlib_model)

video_size = search_video_size(video, predictor, detector, dlib_model)


nb_frame = 0
cap = cv2.VideoCapture(video)

while True:

    start_time_frame = time.time()

    _, frame = cap.read()

    height, width = frame.shape[:2]

    width  = int(width  /  video_size)
    height = int(height /  video_size)


    frame = cv2.resize(frame, (width, height))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Recuperate landmarks and head box.
    landmarks, head_box = head_points(gray, predictor, detector) #face_points


    if landmarks is not None:

        #Recuperate blink algorythme
        blinking_frame, result = blinking_eyes(landmarks, head_box) #blinking_eyes
        blink_analysis(result, nb_frame, blinking_frame) #blinking_eyes

        #Recuperate pupil center, eyes constitution = (x, y), crop
        right_eye, left_eye = pupille_tracker(landmarks, frame, gray)


        movements = eyes_movements(landmarks, frame, right_eye[0], left_eye[0])
        if movements != "":
            print(movements)

  
        eyes_contours(landmarks, frame, right_eye[0], left_eye[0])




        #Draw
        x, y, w, h = head_box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, 'Head', ((x+w) - 30, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)


        if right_eye[0][0] is not None:
            cv2.circle(right_eye[1], (right_eye[0]), 4, (0, 0, 255), 1)
        if left_eye[0][0] is not None:
            cv2.circle(left_eye[1], (left_eye[0]), 4, (0, 0, 255), 1)


        print("No ", nb_frame, "run : ", time.time() - start_time_frame)
        nb_frame += 1



    nb_frame += 1
    cv2.imshow("Frame", frame)


    
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
