from cv2 import VideoCapture, resize, waitKey, destroyAllWindows, imshow, cvtColor, COLOR_BGR2GRAY
from basics_operations import start_timmer, timmer
from face_detection import findHead, headDetector


def video_lecture(video_name):

    video = VideoCapture(video_name)

    #Detect head
    detector = headDetector()

    while True:

        #Timmer start
        start = start_timmer()

        frame = resize(video.read()[1], (400, 300))
        gray = cvtColor(frame, COLOR_BGR2GRAY)

        #Repear head points
        findHead(detector, gray, frame, "displaying")

        imshow('frame', frame)

        #Timmer end
        timmer(start)

        if waitKey(1) & 0xFF == ord("q"):break

    video.release()
    destroyAllWindows()
