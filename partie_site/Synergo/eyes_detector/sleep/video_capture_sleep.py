import time

start_time_import = time.time()

import cv2
import numpy as np

from recuperate_points.face_points import recuperate_landmarks
from recuperate_points.face_points import head_points
from recuperate_points.face_points import get_face_in_box
from recuperate_points.face_points import eyes_points_for_head_analysis


#Pupil part
from pupille_tracker.pupille_tracker import pupille_tracker

#Path to model, to media folder.
from paths import media_path, dlib_model
from paths import path_eyes_detector_stuff

#Blink part
from blinking.blinking_eyes import blinking_eyes
from blinking.blinking_eyes import blink_analysis


#Load dlib model
from recuperate_points.face_points import load_model_dlib


print("Import time : ", time.time() - start_time_import)



def video_capture_to_face(video_name, eyes_image):

    #Recuperate name of the video.
    video  = media_path.format(video_name)

    #Load DLIB.
    predictor, detector = load_model_dlib(dlib_model)


    cap = cv2.VideoCapture(video)

    #Recuperate video informations.
    frame_width  = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_sec = cap.get(cv2.CAP_PROP_FPS)

    out = cv2.VideoWriter("coucou.avi", cv2.VideoWriter_fourcc('M','J','P','G'), int(frame_sec),
                          (frame_width, frame_height))


    while True:

        start_time_frame = time.time()

        _, frame = cap.read()
        height, width = frame.shape[:2]
        frame = cv2.resize(frame, (int(width/2), int(height/2)))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #Recuperate landmarks and head box.
        landmarks, head_box = head_points(gray, predictor, detector) #face_points


        if landmarks is not None:

            #Recuperate blink algorythme
            blinking_frame, result = blinking_eyes(landmarks, head_box) #blinking_eyes
            blink_analysis(result, nb_frame, blinking_frame) #blinking_eyes


        out.write(frame)


        #cv2.imshow("vcsqc", eyes_image)
        cv2.imshow("Frame", frame)

        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


eyes_image = r"C:\Users\jeanbaptiste\Desktop\SYNERGO_SITE\Synergo\media\eyes_detector\gros_oeil.png"
video_capture_to_face("aa.mp4", eyes_image)
