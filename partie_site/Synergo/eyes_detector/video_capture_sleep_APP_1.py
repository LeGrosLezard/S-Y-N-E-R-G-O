import time

start_time_import = time.time()

import cv2
import numpy as np

from .recuperate_points.face_points import recuperate_landmarks
from .recuperate_points.face_points import head_points
from .recuperate_points.face_points import get_face_in_box
from .recuperate_points.face_points import eyes_points_for_head_analysis

#Pupil part
from .pupille_tracker.pupille_tracker import pupille_tracker

#Path to model, to media folder.
from .paths import media_path, dlib_model
from .paths import path_eyes_detector_stuff
from .paths import video_save_media

#Blink part
from .blinking.blinking_eyes import blinking_eyes
from .blinking.blinking_eyes import blink_analysis
from .blinking.blinking_eyes import final

#Load dlib model
from .recuperate_points.face_points import load_model_dlib

print("Import time : ", time.time() - start_time_import)




def displaying(alarm, frame):

    out = False
    
    if alarm[0] is not "":
        cv2.putText(frame, alarm[0], (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        out = True
    if alarm[1] is not "":
        cv2.putText(frame, alarm[1], (0, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,100,255), 2)
        out = True
    if alarm[2] is not "":
        cv2.putText(frame, alarm[2], (0, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36,255,12), 2)
        out = True

    return out

global_alarm = []
def video_capture_to_face_sleep(path_video, video_name):


    cap = cv2.VideoCapture(path_video)

    #Recuperate video informations.
    frame_width  = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_sec = cap.get(cv2.CAP_PROP_FPS)

    video_path = video_save_media.format(video_name + ".mp4")

    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'X264'), 20,
                          (frame_width, frame_height))

    #Load DLIB.
    predictor, detector = load_model_dlib(dlib_model)

    start_time = time.time()
    nb_frame = 0
    continuer = True
    while continuer:

        ret, frame = cap.read()

        if ret:

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Recuperate landmarks and head box.
            landmarks, head_box = head_points(gray, predictor, detector) #face_points


            if landmarks is not None:

                #Recuperate blink algorythme
                blinking_frame, result = blinking_eyes(landmarks, head_box) #blinking_eyes

                timmer = time.time() - start_time
                alarm = blink_analysis(result, nb_frame, blinking_frame, timmer) #blinking_eyes

                to_slow = displaying(alarm, frame)

                if to_slow is True:
                    for i in range(10):
                        out.write(frame)
                else:
                    out.write(frame)
                nb_frame += 1

        else:
            video_length = time.time() - start_time
            continuer = False


    report = final(video_length)

    
    return report, "/media/video_save/" + video_name + ".mp4"

if __name__ == "__main__":
    path_video = r"C:\Users\jeanbaptiste\Desktop\SYNERGO_SITE\Synergo\media\video_upload\g.mp4"
    video_capture_to_face_sleep(path_video, "g.mp4")

