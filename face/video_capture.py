from dlib import get_frontal_face_detector, shape_predictor
from time import time
from cv2 import VideoCapture, resize, waitKey, destroyAllWindows, imshow, cvtColor, COLOR_BGR2GRAY, imwrite
from face.face_detection import recuperate_intra_face_points, intra_face, points_landmarks, exterior_face, inclinaison
from eyes.eyes_detection import tracking_eyes
from display.face_display import recuperate_face


#from face_display import recuperate_face



def start_timmer():
    start = time()
    return start

def timmer(start):
    elapsed = time() - start
    print(elapsed)


def video_lecture(video_name, face_points):

    video = VideoCapture(video_name)

    #Detect head
    detector = get_frontal_face_detector()
    predictor = shape_predictor(face_points)

    right_eye = {"droite":0, "gauche":0, "haut":0, "bas":0}
    left_eye = {"droite":0, "gauche":0, "haut":0, "bas":0}

    while True:

        #Timmer start
        start = start_timmer()

        frame = resize(video.read()[1], (500, 400))
        gray = cvtColor(frame, COLOR_BGR2GRAY)

        #try:
        #68 points of face + face
        landmarks, face = points_landmarks(gray, predictor, detector)

        #Intra Face
        head_points, head, convexhull = recuperate_intra_face_points(landmarks, face, frame)


        #Ext Face
        exterior_face(head, gray)


        #DOIT ETRE UN THREAD
        inclinaison(landmarks, frame)
        leftEye, rightEye = tracking_eyes(landmarks, head, frame, gray, left_eye, right_eye)

        #Doit etre un multiprocess ou thread chpas
        intra_face(frame, gray, landmarks, head, leftEye, rightEye)




        #except (IndexError): pass

 
        #Display
        #recuperate_face(convexhull, gray, frame, head_points)


        #imshow('frame', frame)

        #Timmer end
        timmer(start)

        if waitKey(0) & 0xFF == ord("q"):
            imwrite("ici.jpg", frame)
            break

    video.release()
    destroyAllWindows()
