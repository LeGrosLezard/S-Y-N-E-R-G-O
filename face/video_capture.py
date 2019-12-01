from cv2 import VideoCapture, resize, waitKey, destroyAllWindows, imshow, cvtColor, COLOR_BGR2GRAY, imwrite
from basics_operations import start_timmer, timmer
from points_face.face_detection import headDetector, pointsPredictor, intra_face, points_landmarks


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

        faces = detector(gray)

        #68 points of face
        landmarks = points_landmarks(faces, gray, predictor)

        #Triangle of face points
        head_points, head = intra_face(landmarks, faces, frame)


        imshow('frame', frame)

        #Timmer end
        timmer(start)

        if waitKey(1) & 0xFF == ord("q"):
            imwrite("ici.jpg", frame)
            break

    video.release()
    destroyAllWindows()
