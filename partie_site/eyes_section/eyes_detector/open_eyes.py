import cv2
import numpy as np

def eyes_position(landmarks, frame, right_eye, left_eye):

    eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                    for n in range(36, 42)])),
            cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                    for n in range(42, 48)])))

    cv2.drawContours(frame, [eyes[0]], -1, (0, 255, 0), 1)
    cv2.drawContours(frame, [eyes[1]], -1, (0, 255, 0), 1)

    print(right_eye)
    print(left_eye)
    print("")
