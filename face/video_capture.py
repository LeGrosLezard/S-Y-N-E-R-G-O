from cv2 import VideoCapture, resize, waitKey, destroyAllWindows, imshow, cvtColor, COLOR_BGR2GRAY, imwrite
from basics_operations import start_timmer, timmer
from points_face.face_detection import headDetector, pointsPredictor, intra_face, points_landmarks
from points_face.face_display import recuperate_face

def video_lecture(video_name, face_points):

    video = VideoCapture(video_name)

    #Detect head
    detector = headDetector()
    predictor = pointsPredictor(face_points)


    while True:

        #Timmer start
        start = start_timmer()

        frame = resize(video.read()[1], (500, 400))
        gray = cvtColor(frame, COLOR_BGR2GRAY)

        #68 points of face + face
        landmarks, face = points_landmarks(gray, predictor, detector)

        #Triangle of face points
        head_points, head, convexhull = intra_face(landmarks, face, frame)

        #Display
        recuperate_face(convexhull, gray, frame, head_points)
        

        #imshow('frame', frame)

        #Timmer end
        timmer(start)

        if waitKey(1) & 0xFF == ord("q"):
            imwrite("ici.jpg", frame)
            break

    video.release()
    destroyAllWindows()
