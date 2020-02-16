import cv2
import dlib
import numpy as np

#Recuperate points.
from face_points import recuperate_landmarks
#Recuperate face in square.
from face_points import get_face_in_box


def resizer(frame, predictor, detector):

    video_division = 0.35   #Increment this var for video size.
    height, width = frame.shape[:2] #Initial dimension of the video.

    find = False    #We loop until find a width face.
    ocontinue = True    #Loop condition.
    while ocontinue:

        video_division += 0.05  #Incrementation.
        width  = int(width /  video_division)   #Divide width.
        height = int(height / video_division)   #Divide height.

        if width > 2000 or height > 2000:   #Regulation of the hights dimensions.
            pass

        elif width < 50 or height < 50: #Regulation of the smaller dimensions.
            ocontinue = False


        elif width > 0 and height > 0:  #Ok dimension.

            frame = cv2.resize(frame, (width, height))  #Resize the frame.
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Gray threshold.

            #Recuperate landmarks.
            faces, landmarks = recuperate_landmarks(gray, predictor, detector)

            #Regulation of no landmarks.
            if landmarks is not None:
                head = get_face_in_box(landmarks)   #Box the face.
                x, y, w, h = head   #Recuperate the square box face.
                #print(w, y, video_division) #Display dimension

                if w <= 93: #We exceed 93 width pixels.
                    find = True #Condition for stop loop from main.
                    ocontinue = False #Condition for stop the current loop.


            #Higtly recommande if first time watch.
            #cv2.imshow("frameframe", frame)
            #cv2.waitKey(0)



    return video_division, find



def search_video_size(video, predictor, detector, dlib_model):

    #Initialise video.
    cap = cv2.VideoCapture(video)

    #Loop condition.
    search_video_size = True
    while search_video_size:

        _, frame = cap.read() #Window
        #Search dimensions.
        video_size, find = resizer(frame,  predictor, detector)

        if find is True:    #We found a dimensions.
            search_video_size = False

    return video_size
