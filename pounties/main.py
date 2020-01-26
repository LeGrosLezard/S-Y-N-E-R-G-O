import cv2


from hands.hand_detection.hand_detection import hands_detections
from hands.hand_detection.hand_detection import detect_objects
from hands.hand_detection.hand_detection import load_inference_graph

from hands.hand_treatment.hand_mask import skin_detector
from hands.hand_treatment.hand_mask import hand_treatment
from hands.hand_treatment.hand_mask import make_bitwise


from hands.hand_treatment.skeletton import hand_skelettor

from main_utils import hand_dection_part
from main_utils import hand_isolation_part



path_to_ckpt = r"C:\Users\jeanbaptiste\Desktop\frozen_inference_graph.pb"
protoFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_deploy.prototxt"
weightsFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_iter_102000.caffemodel"


detection_graph, sess = load_inference_graph(path_to_ckpt)






cap = cv2.VideoCapture("videos/a.mp4")

nb = 2

while True:

    _, frame = cap.read()
    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (int(width / nb), int(height / nb)))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detections = hand_dection_part(frame, detection_graph, sess)

    for nb, hand in enumerate(detections):

        hand_masked, rectangle = hand_isolation_part(hand, frame, frame_copy)

        _, points, _ = hand_skelettor(hand_masked, protoFile, weightsFile)

        print(points)



    
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
 
cap.release()
cv2.destroyAllWindows()








