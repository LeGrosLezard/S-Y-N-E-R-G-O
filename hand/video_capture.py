import cv2
import tensorflow as tf
import numpy as np
from time import time
import imutils
from utils import load_inference_graph, detect_objects


print(tf.version.VERSION)

def start_timmer():
    start = time()
    return start

def timmer(start):
    elapsed = time() - start
    print(elapsed)

def sustractor_background(frame, fgbg):
    """Delete background, if one thing moves we detect it"""

    suba = fgbg.apply(frame)
    contours, _ = cv2.findContours(suba, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for cnts in contours:
        if 1000 > cv2.contourArea(cnts) > 250:
            x, y, w, h = cv2.boundingRect(cnts)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 3, 1)

    liste = [(cv2.boundingRect(cnts)[0], cv2.boundingRect(cnts)[1], cv2.boundingRect(cnts)[0] + cv2.boundingRect(cnts)[2],
             cv2.boundingRect(cnts)[1] + cv2.boundingRect(cnts)[3]) for cnts in contours if 1000 > cv2.contourArea(cnts) > 250]

    return liste


def hands_detections(scores, boxes, droite, gauche, hist_droite, hist_gauche, frame):
    """We detect hands, by position we define if it are to left or to right.
    Recup it for history if we have impossible detections"""

    detected_points = [(int(boxes[i][1] * 500), int(boxes[i][3] * 500),
                        int(boxes[i][0] * 400), int(boxes[i][2] * 400)) for i in range(2) if scores[i] > 0.10]

    right_left_points = [  [(pt[0], pt[2], pt[1], pt[3]) for pt in detected_points if pt[0] < 250],
                           [(pt[0], pt[2], pt[1], pt[3]) for pt in detected_points if pt[0] > 250]   ]

    def append_to_hand(hand, movement, historic, part):
        """Add movements to his list"""

        if len(movement[part]) >= 1:
            hand.append(movement[part][0])
            historic[0].append(movement[part][0][0])
            historic[1].append(movement[part][0][1])

    append_to_hand(droite, right_left_points, hist_droite, 0)
    append_to_hand(gauche, right_left_points, hist_gauche, 1)


def possibles_movement(historic, movement, possibility):
    """By history if we have x and y axis > 60: impossible move"""

    nb = 60
    if abs(historic[0][-1] - historic[0][-2]) > nb or\
       abs(historic[1][-1] - historic[1][-2]) > nb:
        possibility = "impossible"
        movement.remove(movement[-1])

    return possibility


def detections_from_substractor(points_movements, movement):
    """Recup all movement by substractor, recup min x and y and max width and height
    It make all the hand"""

    points = [[], [], [], []]; x_w = 70; y_h = 100

    for i in points_movements:
        a = abs(i[0] - movement[0][0])
        b = abs(i[1] - movement[0][1])
        c = abs(i[2] - movement[0][2])
        d = abs(i[3] - movement[0][3])

        if a < x_w and b < y_h and c < x_w and d < y_h:
            points[0].append(i[0])
            points[1].append(i[1])
            points[2].append(i[2])
            points[3].append(i[3])

    return points



def draw(frame, points_movements):
    """Draw all movement close to the hand"""

    if len(points_movements[0]) != 0:
        cv2.rectangle(frame, (min(points_movements[0]), min(points_movements[1])),
                             (max(points_movements[2]), max(points_movements[3])),
                      (77, 0, 0), 3, 1)


def no_hand_detection(movement, points_movements, historic):
    """ No hand detection (right or left) We make a detection
    thank to movement by substractor in comparaison to the last hand detection.
    Course we define this detection like a hand detection."""

    if len(movement) == 1 and len(points_movements[0]) != 0:

        movement.append((min(points_movements[0]), min(points_movements[1]),
                         max(points_movements[2]), max(points_movements[3])))

        historic[0].append(min(points_movements[0]))
        historic[1].append(min(points_movements[1]))

def fusion_movement_detection(movement, points_movements):
    """Merge movement substractor with hand model detection"""

    if len(movement) == 2 and len(points_movements[0]) != 0:
        fusion = [[], [], [], []]

        for i in range(4):
            fusion[i].append(movement[-1][i])

        for nb, i in enumerate(points_movements):
            for j in i:
                fusion[nb].append(j)

        movement[-1] = (min(fusion[0]), min(fusion[1]), max(fusion[2]), max(fusion[3]))


def false_hand_detection(possibility, points_movements, movement):
    """By history we observ a impossible detection, so we delete it from
    the movement list and replace it by movement substracor detection"""

    if possibility == "impossible" and len(points_movements[0]) != 0:
        movement[-1] = ((min(points_movements[0]), min(points_movements[1]),
                       max(points_movements[2]), max(points_movements[3])))


def more_than_one_detection(movement):
    """Sometime it can be 2 right or 2 left detections. We recup
    the higther detection from the last hand detection"""

    #ICIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII

    if len(movement) == 3:
        if (movement[0][0] - movement[1][0]) < (movement[0][0] -  movement[2][0]):
            movement[-1] = movement[-2]


def detections(movement, points_movements, historic, possibility, frame):
    """We look history.
    History compare last hand detection with the new one.
    We compare x and y. If last and actual are < 60 px we keep it. Else
    We delete it and send possibility or no possible.

    After we make a substractor of background who's detect all movements
    all news element on the scene.

    We drawing it to the screen (red rectangles).

    If we havent got any detection, We ask last hand model detection and recup
    all background movement detection in 100 closed px. We define it like a hand detection.

    No we include hand model detection + movement background around 100 px.

    If we had detected a impossible detection from the hand model we define
    our hand detection by the backougrnd movement.

    Finally we have more than one detection on a side (2 hand model detection on right for example)
    so we recuperate the highter x from the last hand model detection.

    We define our hand model detection like the last detection if we got it.
    Else we define movement backougrnd detection in function of last hand model detection like
    our last detection.

    """

    if len(historic[0]) >= 2 and len(movement) >= 1:
        possibility = possibles_movement(historic, movement, possibility)
    
    if len(movement) >= 1:
        droite_points = detections_from_substractor(points_movements, movement)
        draw(frame, droite_points)
        no_hand_detection(movement, droite_points, historic)
        fusion_movement_detection(movement, droite_points)
        false_hand_detection(possibility, droite_points, movement)
        more_than_one_detection(movement)

        cv2.rectangle(frame, (movement[-1][0], movement[-1][1]),
                       (movement[-1][2], movement[-1][3]), (77, 255, 9), 3)

        movement = [movement[-1]]

    return movement


def video_capture(video_name, hand_model):

    detection_graph, sess = load_inference_graph(hand_model)
    video = cv2.VideoCapture(video_name)
    fgbg = cv2.createBackgroundSubtractorMOG2(history=120, detectShadows=False)

    droite = []; gauche = []; hist_droite = [[], []]; hist_gauche = [[], []]

    while True:

        possible_droite = "possible"; possible_gauche = "possible"

        start = start_timmer()

        frame = cv2.resize(video.read()[1], (500, 400))
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        points_movements = sustractor_background(frame, fgbg)

        boxes, scores = detect_objects(frameRGB, detection_graph, sess)
        hands_detections(scores, boxes, droite, gauche, hist_droite, hist_gauche, frame)

        droite = detections(droite, points_movements, hist_droite, possible_droite, frame)
        gauche = detections(gauche, points_movements, hist_gauche, possible_gauche, frame)



        








        timmer(start)


        cv2.imshow("mask", frame)


        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
