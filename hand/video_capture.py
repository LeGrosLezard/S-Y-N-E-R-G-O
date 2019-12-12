from cv2 import VideoCapture, resize, cvtColor, COLOR_BGR2RGB, imshow, waitKey, destroyAllWindows, rectangle
from hand_detection.utils import load_inference_graph, detect_objects
from hand_detection.hand_detection import hands_detections
from hand_signification.skelettor import make_skelettor
import tensorflow as tf



def video_capture(video_name, hand_model, hand_skelettor_PROTXT, hand_skelettor_CAFFE):

    detection_graph, sess = load_inference_graph(hand_model)
    video = VideoCapture(video_name)

    while True:

        frame = resize(video.read()[1], (500, 400))
        copy = frame.copy()

        frameRGB = cvtColor(frame, COLOR_BGR2RGB)

        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        detections = hands_detections(scores, boxes, frame)

        nb = 40
        for hand in detections:
            if len(hand) > 0:
                rectangle(frame, (hand[0] - nb, hand[1] - nb), (hand[2] + nb, hand[3] + nb), (79, 220, 25), 4)


        imshow("frame", frame)
        if waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()





















