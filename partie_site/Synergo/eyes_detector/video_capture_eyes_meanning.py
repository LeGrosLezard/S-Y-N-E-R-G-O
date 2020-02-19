import time
import cv2
import os

import numpy as np

#Load dlib model
from recuperate_points.face_points import load_model_dlib

from recuperate_points.face_points import recuperate_landmarks
from recuperate_points.face_points import head_points
from recuperate_points.face_points import get_face_in_box
from recuperate_points.face_points import eyes_points_for_head_analysis

#Pupil part
from pupille_tracker.pupille_tracker import pupille_tracker

from paths import media_path, dlib_model, path_data, path_data_video, path_csv_file



def recuperate_eyes_mean_position(video):

    cap = cv2.VideoCapture(video)
    predictor, detector = load_model_dlib(dlib_model)

    #height, width = frame.shape[:2]
    height= 505
    width = 673
    BLANCK = np.zeros((height,width,3), np.uint8)
    
    while True:

        start_time_frame = time.time()

        ret, frame = cap.read()

        if ret:

            b, a = frame.shape[:2]
            #frame = cv2.resize(frame, (int(a / 1.1000000000000003), int(b / 1.1000000000000003)))#a
            #frame = cv2.resize(frame, (int(a / 1.3244035243988037), int(b / 1.3244035243988037)))#ca
            #frame = cv2.resize(frame, (int(a /  0.8500000000000002), int(b /  0.8500000000000002)))#ca
            #frame = cv2.resize(frame, (int(a /   1.4000000000000006), int(b /   1.4000000000000006)))#aaa
            frame = cv2.resize(frame, (int(a /   0.9500000000000003), int(b /   0.9500000000000003)))
            b, a = frame.shape[:2]



            #Gray threshold.
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            #Recuperate landmarks and head box.
            landmarks, head_box = head_points(gray, predictor, detector) #face_points

            if landmarks is not None:

                #Recuperate pupil center, eyes constitution = (x, y), crop
                right_eye, left_eye = pupille_tracker(landmarks, frame, gray, head_box, BLANCK)

            cv2.imshow("Frame", frame)
            cv2.imshow("BLANCK", BLANCK)
            #print(time.time() - start_time_frame)

            if cv2.waitKey(0) & 0xFF == ord('q'):
                return "stop"




    cap.release()
    cv2.destroyAllWindows()



def number_of_file(path_data):

    data = os.listdir(path_data)
    data = sorted(data)
    number_file = len(data)

    print("Count file to treat : ", number_file)

    return data, number_file




data, number_file = number_of_file(path_data)

for video in data:
    video = path_data_video.format(video)
    #video = path_data_video.format("a.mp4")
    #video = path_data_video.format("b.mp4")
    #video = path_data_video.format("c.mp4")
    #video = path_data_video.format("aaa.mp4")
    video = path_data_video.format("e.mp4")

    print("in course: ", video)
    
    stop = recuperate_eyes_mean_position(video)
    if stop == "stop":
        break






