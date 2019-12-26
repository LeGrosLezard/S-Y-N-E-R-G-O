import cv2
import numpy as np
import dlib
from dlib import get_frontal_face_detector, shape_predictor


from paths import dlib_model

#Treat video for have 90 px width head.
from video_treatment import resize_frame

#Load DLIB model and Recuperate Landmarks and head.
from head_points import load_model_dlib, head_points

#Blink part
from blinking_eyes import blinking_eyes
from analysis_eyes import blink_analysis


#Pupil part
from pupille_tracker import pupille_tracker
#Eyes movement part
from eyes_movement import eyes_position




#Load dlib model
predictor, detector = load_model_dlib(dlib_model)


nb_frame = 0
cap = cv2.VideoCapture("a.mp4")

while True:
   
    _, frame = cap.read()

    #Resize frame for have 90 px head width.
    frame, gray = resize_frame(frame)

    #Recuperate landmarks and head box.
    landmarks, head_box = head_points(gray, predictor, detector)


    if landmarks is not None:


        #Recuperate blink algorythme
        blinking_frame, result = blinking_eyes(landmarks, head_box)
        blink_analysis(result, nb_frame, blinking_frame)

        #Recuperate pupil center
        right_eye, left_eye = pupille_tracker(landmarks, frame, gray)
        eyes_position(landmarks, frame, right_eye, left_eye)






    nb_frame += 1
    cv2.imshow("Frame", frame)

    
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
