from dlib import get_frontal_face_detector, shape_predictor
import numpy as np
import cv2




#===================================================== Video part
def resize_frame(frame):
    """Resize frame for a ' good accuracy ' and speed """
 
    height, width = frame.shape[:2]
    nb = 2
    frame = cv2.resize(frame, (int(width / nb), int(height / nb)))
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    return frame, gray


#===================================================== Landmarks part
def recuperate_landmarks(gray):

    faces = detector(gray)
    if len(faces) > 0:
        landmarks = predictor(gray, faces[0])
        out = faces, landmarks
    else:
        out = None, None    #No face detected = no landmarks

    return out


def recuperate_eyes(landmarks):

    if landmarks is not None:
        eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                        for pts in faces for n in range(36, 42)])),
                cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                        for pts in faces for n in range(42, 48)])))
        out = eyes
    else:
        out = None  #No landmarks

    return out



#===================================================== Mask part
def rectangle_eye_area(img, eye, gray):
    """Recuperate contour of eyes in a box, make an egalizer,
    make a color and gray mask."""

    nb = 5
    x, y, w, h = cv2.boundingRect(eye)
    cropMask = gray[y-nb:y+h+nb, x-nb:x+w+nb]
    cropMask = cv2.equalizeHist(cropMask)

    cropImg = img[y-nb:y+h+nb, x-nb:x+w+nb]

    return cropMask, cropImg


def eye_contour_masking(img, eye, gray):
    """Recuperate contour of eyes points, delimitate that
    recuperate color and gray mask."""

    nb = 5
    height, width = gray.shape[:2]
    black_frame = np.zeros((height, width), np.uint8)
    mask = np.full((height, width), 255, np.uint8)
    cv2.fillPoly(mask, [eye], (0, 0, 255))
    mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)

    x, y, w, h = cv2.boundingRect(eye)
    cropMask = mask[y-nb:y+h+nb, x-nb:x+w+nb]
    cropImg = img[y-nb:y+h+nb, x-nb:x+w+nb]

    return cropMask, cropImg


def superpose_contour_eye_rectangle(mask_eyes_gray, crop):
    for i in range(mask_eyes_gray.shape[0]):
        for j in range(mask_eyes_gray.shape[1]):
            if mask_eyes_gray[i, j] == 255:
                crop[i, j] = 255
    return crop



#===================================================== Pupille center part

def find_center_pupille(crop, mask_eyes_img):
    """Find contours. Don't recuperate rectangle contour,
    find centers."""

    contours, hierarchy = cv2.findContours(crop, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    height, width = mask_eyes_img.shape[:2]
    percent_contour = 0.80

    pupille_center = [(int(cv2.moments(cnt)['m10']/cv2.moments(cnt)['m00']),
                       int(cv2.moments(cnt)['m01']/cv2.moments(cnt)['m00']))
                      for cnt in contours if cv2.contourArea(cnt) < (percent_contour * (width * height))]

    if len(pupille_center) > 0:
        x_center, y_center = pupille_center[0][0], pupille_center[0][1]
        cv2.circle(mask_eyes_img, (x_center, y_center), 4, (0, 0, 255), 1)
        out = x_center, y_center
    else:
        out = None, None    #no pupils detected

    return out


def main_function_pupille_part(eye):
    """Recuperate egalized rectangle area or box area,
       recuperate contour eyes,
       Superpose egalized rectangle with contour eyes,
       find centers"""

    #Box egalized eyes areas
    gray_crop, color_crop = rectangle_eye_area(frame, eye, gray)
    #Contours of the broder of the eyes
    mask_eyes_gray, mask_eyes_img = eye_contour_masking(frame, eye, gray)
    #Superpose box and contours
    gray_crop = superpose_contour_eye_rectangle(mask_eyes_gray, gray_crop)
    #Define centers of pupils
    x_center, y_center = find_center_pupille(gray_crop, mask_eyes_img)

    return x_center, y_center







video = cv2.VideoCapture("a.mp4")
detector = get_frontal_face_detector()
predictor = shape_predictor("shape_predictor_68_face_landmarks.dat")


while True:

    _, frame = video.read()
    frame, gray = resize_frame(frame)


    faces, landmarks = recuperate_landmarks(gray)
    eyes = recuperate_eyes(landmarks)

    if eyes is not None:

        right_eyes = eyes[0]
        main_function_pupille_part(right_eyes)

        left_eyes = eyes[1]
        main_function_pupille_part(left_eyes)





    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


