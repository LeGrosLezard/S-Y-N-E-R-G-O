import cv2

def hand_dection_part(frame, detection_graph, sess):

    frame_copy = frame.copy()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, scores = detect_objects(frameRGB, detection_graph, sess)

    detections = hands_detections(scores, boxes, frame)

    return detections

def hand_isolation_part(hand, frame, frame_copy):
    skinYCrCb, crop, copy = skin_detector(hand, frame, frame_copy)
    contours = hand_treatment(skinYCrCb, crop)
    hand_masked, rectangle = make_bitwise(contours, copy)

    return hand_masked, rectangle
