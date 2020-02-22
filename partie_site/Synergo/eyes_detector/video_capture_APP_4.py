import time

start_time_import = time.time()

import cv2
import numpy as np

from .recuperate_points.face_points import recuperate_landmarks
from .recuperate_points.face_points import head_points
from .recuperate_points.face_points import get_face_in_box
from .recuperate_points.face_points import eyes_points_for_head_analysis


#Blink part
from .blinking.blinking_eyes import blinking_eyes
from .blinking.blinking_eyes import blink_analysis

#Pupil part
from .pupille_tracker.pupille_tracker import pupille_tracker

#Path to model, to media folder.
from .paths import media_path, dlib_model

#Load dlib model
from .recuperate_points.face_points import load_model_dlib

#Resize video.
from .pre_treatment.pre_test import search_video_size

#Drawing into the video.
from .drawing.drawing import draw


print("Import time : ", time.time() - start_time_import)


def video_capture(video):

    video  = media_path.format(video)
    predictor, detector = load_model_dlib(dlib_model)

    nb_frame = 0
    cap = cv2.VideoCapture(video)

    while True:

        start_time_frame = time.time()

        _, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Recuperate landmarks and head box.
        landmarks, head_box = head_points(gray, predictor, detector) #face_points

        if landmarks is not None:

            #Recuperate blink algorythme
            blinking_frame, result = blinking_eyes(landmarks, head_box) #blinking_eyes
            blink_analysis(result, nb_frame, blinking_frame, start_time_frame) #blinking_eyes

            #Recuperate pupil center, eyes constitution = (x, y), crop
            right_eye, left_eye = pupille_tracker(landmarks, frame, gray, head_box)

            movements = eyes_movements(landmarks, frame, right_eye[0], left_eye[0])
            if movements != "":
                print(movements)

            eyes_contours(landmarks, frame, right_eye[0], left_eye[0])

            draw(head_box, frame, right_eye, left_eye)

            print("No ", nb_frame, "run : ", time.time() - start_time_frame)
            nb_frame += 1


        nb_frame += 1
##        cv2.imshow("Frame", frame)
##
##        if cv2.waitKey(0) & 0xFF == ord('q'):
##            break
##
##    cap.release()
##    cv2.destroyAllWindows()
