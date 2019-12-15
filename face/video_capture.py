from dlib import get_frontal_face_detector, shape_predictor
from time import time
from cv2 import VideoCapture, resize, waitKey, createBackgroundSubtractorMOG2, destroyAllWindows, imshow, cvtColor, COLOR_BGR2GRAY, imwrite
from face.face_detection import recuperate_intra_face_points, intra_face, points_landmarks, exterior_face, inclinaison, emotion_points, emotions_model, expressions
from eyes.eyes_detection import tracking_eyes

from display.face_display import face_displaying
from display.eyes_display import eyes_display

#from face_display import recuperate_face



def start_timmer():
    start = time()
    return start

def timmer(start):
    elapsed = time() - start
    print(elapsed)


def video_capture(video_name, face_points, emotion_model):

    video = VideoCapture(0)

    #Detect head
    detector = get_frontal_face_detector()
    predictor = shape_predictor(face_points)

    right_eye = {"right":0, "left":0, "top":0, "bot":0}
    left_eye = {"right":0, "left":0, "top":0, "bot":0}

    em_nose = [[], []]
    open_right_eye = [[], []]
    open_left_eye = [[], []]
    eye_display = []

    counter_frame = 0
    while True:

        #Timmer start
        start = start_timmer()

        frame = resize(video.read()[1], (500, 400))
        gray = cvtColor(frame, COLOR_BGR2GRAY)

        try:
            #68 points of face + face
            landmarks, face = points_landmarks(gray, predictor, detector)

            #Intra Face
            head, convexhull = recuperate_intra_face_points(landmarks, face, frame)


            #Ext Face
            exterior_face(head, gray)


            #DOIT ETRE UN THREAD
            inclinaison(landmarks, frame)
            eyes_movements = tracking_eyes(landmarks, head, frame, gray, left_eye, right_eye)

            #Doit etre un multiprocess ou thread chpas
            intra_face(frame, gray, landmarks, head)
            #emotion_points(frame, landmarks, em_nose, open_right_eye, open_left_eye)
            #expressions(counter_frame, em_nose, open_right_eye, open_left_eye)


        
     
            #Display
            face_displaying(gray, frame, convexhull, landmarks)

            #raising = eyes_display(frame, gray, landmarks, eyes_movements, eye_display, counter_frame)





        except (IndexError): pass
        imshow('frame', frame)

        #Timmer end
        #timmer(start)
        raising = False

        if raising == True:
            eye_display = []

        counter_frame += 1

        if waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    destroyAllWindows()
