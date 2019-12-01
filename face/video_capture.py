from cv2 import VideoCapture, resize, waitKey, destroyAllWindows, imshow, cvtColor, COLOR_BGR2GRAY, imwrite
from basics_operations import start_timmer, timmer
from points_face.face_detection import findHead, headDetector


def video_lecture(video_name, face_points):

    video = VideoCapture(video_name)

    #Detect head
    detector = headDetector()
    predictor = pointsPredictor(gray, head, face_points)


    while True:

        #Timmer start
        start = start_timmer()

        frame = resize(video.read()[1], (500, 400))
        gray = cvtColor(frame, COLOR_BGR2GRAY)

        #Repear head points
        head = findHead(detector, gray, frame, "no_displaying")

        imshow('frame', frame)

        #Timmer end
        timmer(start)

        if waitKey(1) & 0xFF == ord("q"):
            imwrite("ici.jpg", frame)
            break

    video.release()
    destroyAllWindows()
