from dlib import get_frontal_face_detector, shape_predictor
from time import time
from cv2 import VideoCapture, resize, waitKey, createBackgroundSubtractorMOG2, destroyAllWindows, imshow, cvtColor, COLOR_BGR2GRAY, imwrite
from face.face_detection import recuperate_intra_face_points, intra_face, points_landmarks, exterior_face, inclinaison, emotion_points, emotions_model
from eyes.eyes_detection import tracking_eyes, position, close_eyes_frequency

from display.face_display import face_displaying, emotion_points_display
from display.eyes_display import eyes_display

#from face_display import recuperate_face



def start_timmer():
    start = time()
    return start

def timmer(start):
    elapsed = time() - start
    print(elapsed)


def video_capture(video_name, face_points, emotion_model):

    video = VideoCapture(video_name)

    #Detect head
    detector = get_frontal_face_detector()
    predictor = shape_predictor(face_points)

    right_eye = {"right":0, "left":0, "top":0, "bot":0}
    left_eye = {"right":0, "left":0, "top":0, "bot":0}

    points_position = [[], [], []]
    closed_list = [0]

    em_nose = [[], []]
    open_right_eye = []
    open_left_eye = []

    mouse_top = [[], [], []]
    mouse_bot = [[], [], []]

    mouse_x = [[], []]
    smyling = []

    on_eye_right = []
    on_eye_left = []


    eye_display = []


    counter_frame = 1
    while True:

        #Timmer start
        start = start_timmer()

        frame = resize(video.read()[1], (500, 400))
        gray = cvtColor(frame, COLOR_BGR2GRAY)

        try:
            #68 points of face + face
            landmarks, face = points_landmarks(gray, predictor, detector)

            plan = position(landmarks, points_position)
            if plan is True:
                points_position = [[], [], []]


            #Intra Face
            head, convexhull = recuperate_intra_face_points(landmarks, face, frame)

        

            eyes_movements = tracking_eyes(landmarks, head, frame, gray, left_eye, right_eye)
            close_eyes_frequency(eyes_movements, closed_list, counter_frame)


            #Ext Face
            #exterior_face(head, gray, landmarks)


            #DOIT ETRE UN THREAD
            #inclinaison(landmarks, frame)

            #Doit etre un multiprocess ou thread chpas
            #intra_face(frame, gray, landmarks, head)

            #emotion_points(frame, landmarks, em_nose, open_right_eye, open_left_eye, mouse_top,
            #                           mouse_bot, mouse_x, on_eye_right, on_eye_left, smyling,
            #                          counter_frame)




        
     
            #Display
            raising = eyes_display(frame, gray, landmarks, eyes_movements, eye_display, counter_frame)


            #face_displaying(gray, frame, convexhull, landmarks)
            #emotion_points_display(frame, landmarks)




        except (IndexError): pass
        imshow('frame', frame)

        #Timmer end
        #timmer(start)
        raising = False

        if counter_frame % 20 == 0:
            open_right_eye = open_right_eye[-10:]
            points_position = [points_position[0][-10:], points_position[1][-10:], points_position[2][-10:]]
            closed_list = closed_list[-10:]

        counter_frame += 1

        if waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    destroyAllWindows()
