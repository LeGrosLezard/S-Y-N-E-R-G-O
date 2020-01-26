import cv2

from hands.hand_detection.hand_detection import hands_detections
from hands.hand_detection.hand_detection import detect_objects


def hand_dection_part(frame, detection_graph, sess):

    frame_copy = frame.copy()
    frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    boxes, scores = detect_objects(frameRGB, detection_graph, sess)

    detections = hands_detections(scores, boxes, frame)

    return detections, frame_copy


from hands.hand_treatment.hand_mask.hand_mask import skin_detector
from hands.hand_treatment.hand_mask.hand_mask import hand_treatment
from hands.hand_treatment.hand_mask.hand_mask import make_bitwise

def hand_isolation_part(hand, frame, frame_copy):

    skinYCrCb, crop, copy = skin_detector(hand, frame, frame_copy)
    contours = hand_treatment(skinYCrCb, crop)
    hand_masked, rectangle = make_bitwise(contours, copy)

    return hand_masked, rectangle




from hands.hand_treatment.clean_skeletton.finger_found import finger_found
from hands.hand_treatment.clean_skeletton.palm_analyse import palm_analyse
from hands.hand_treatment.clean_skeletton.thumb_location import thumb_location
from hands.hand_treatment.clean_skeletton.delete_phax import delete_phax
from hands.hand_treatment.clean_skeletton.delete_finger import delete_finger
from hands.hand_treatment.clean_skeletton.identify_fingers import identify_fingers

LAST_FINGERS_LEFT = []
LAST_FINGERS_RIGHT = []

def treat_skeletton_points(skeletton, position, finger, rectangle, crop):

    global LAST_FINGERS_RIGHT
    global LAST_FINGERS_LEFT

    x, y, w, h = rectangle
    print("Box de la main est de :", rectangle)

    palm_center =  position[0][0]
    palm = [position[5][0], position[9][0], position[13][0], position[17][0], position[0][1]]

    thumb = position[1:4]; index = position[5:8]; major = position[9:12]; annular = position[13:16]
    auricular = position[17:20]


    fingers = finger_found(finger, thumb, index, major, annular, auricular)
    thumb_localisation = thumb_location(fingers, crop)

    if thumb_localisation is not False:

        palm_analyse(thumb_localisation, palm_center, palm, rectangle, crop, fingers)

        sorted_fingers = delete_phax(fingers, LAST_FINGERS_RIGHT, crop)

        sorted_fingers = delete_finger(sorted_fingers, crop)

        finger_sorted = identify_fingers(sorted_fingers[0], sorted_fingers[1:], crop, rectangle)


        print(position[0][0], finger_sorted)
        return [position[0][0]], finger_sorted


    if thumb_localisation is False:
        print("no thumb found")
        return None


def retreat_points(palm_center, points_sorted):

    reput_center_palm = []
    for i in points_sorted:
        if i[1] == "thumb":
            i = palm_center + i[0]
        reput_center_palm.append(i)

    put_finger_order = []
    put_finger_order.append(aa[-1])
    put_finger_order += [i[0] for i in reput_center_palm[:-1]]

    all_points = [j for i in bb for j in i]

    reorganize_by_pair = []
    for i in range(len(all_points)):
        if i == 0:
            reorganize_by_pair.append((all_points[0], all_points[1]))
        else:
            if i < len(b) -1:
                reorganize_by_pair.append((all_points[i], all_points[i + 1]))

    return reorganize_by_pair
