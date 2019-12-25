"""here eyes_movements"""


import cv2
import numpy as np
import dlib




cap = cv2.VideoCapture("a.mp4")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")


while True:
   
    _, frame = cap.read()

    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (int(width/2), int(height/2)))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    


    cv2.imshow("Frame", frame)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()
