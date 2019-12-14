import cv2
from numpy import array, hstack, zeros_like

def eyes_animations(frame, eye):

    #Crop
    x, y, w, h = cv2.boundingRect(eye)
    eye = frame[y-10:y+h, x:x+w]

    #Resize
    height, width = eye.shape[:2]
    eye = cv2.resize(eye, (width*10, height*8))

    #Make border
    height_frame, width_frame = frame.shape[:2]

    #Take 1/2 of frame, crop dimensions
    h_diff = int((height_frame - height) / 2)
    w_diff = int((width_frame - width) / 2)

    #Make border
    eye = cv2.copyMakeBorder(eye, top=h_diff,bottom=h_diff,left=w_diff,right=w_diff,
                             borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])

    return eye, h_diff, w_diff, x, y, w, h


def animations(h, w, x1, y1, w1, h1, eye, eye_display):

    dr = 0
    ga = 0
    ha = 0
    ba = 0
    movement = []
    if eye_display != []:
        for i in eye_display:
            if i == "droite":
                dr += 1
            if i == "gauche":
                ga += 1

            if i == "haut":
                ha += 1

            if i == "bas":
                ba += 1

    if dr > 0 and ha > 0:
        movement.append("droite haut")

    elif dr > 0 and ba > 0:
        movement.append("droite bas")

    elif ga > 0 and ha > 0:
        movement.append("gauche haut")

    elif ga > 0 and ha > 0:
        movement.append("gauche bas")

    elif dr > 0:
        movement.append("droite")

    elif ga > 0:
        movement.append("gauche")





    aa = int(((y1+h1)) + h - 90)
    a = int(((y1+h1)) + h - 30)
    aaa = int(((y1+h1)) + h + 30)


    moves = {"droite":[(w, a), (w - 200, a), (w - 200 + 30, a + 30), (w - 200 + 30, a - 30)],
             "droite haut":[(w, aa), (w - 100, aa - 100), (w - 100, aa - 100 + 30), (w - 100 + 30, aa - 100)],
             "droite bas":[(w, aaa), (w - 100, aaa + 100), (w - 100 + 30, aaa + 100), (w - 100, aaa + 100 - 30)],
             "gauche":[(w + 140, a), (w + 340, a), (w + 340 - 30, a - 30), (w + 340 - 30, a + 30)],
             "gauche haut":[(w + 140, aa), (w + 240, aa - 100), (w + 240, aa - 100 + 30), (w + 240 - 30, aa - 100)],
             "gauche bas":[(w + 140, aaa), (w + 240, aaa + 100), (w + 240 - 30, aaa + 100), (w + 240, aaa + 100 - 30)]}

    watch = ""
    for i in movement:
        for k,v in moves.items():
            if i == k:
                cv2.line(eye, (v[0][0], v[0][1]), (v[1][0], v[1][1]), (0, 0, 255), 3)
                cv2.line(eye, (v[1][0], v[1][1]), (v[2][0], v[2][1]), (0, 0, 255), 3)
                cv2.line(eye, (v[1][0], v[1][1]), (v[3][0], v[3][1]), (0, 0, 255), 3)

                watch += k
    

    
    if watch == "":
        watch = "center"

    return eye, watch




def eyes_display(frame, gray, landmarks, eyes_movements, eye_display, counter_frame):

    raising = False

    if eyes_movements != None:
        for i in eyes_movements:
            eye_display.append(i)

    if eye_display != [] and eyes_movements == None:
        raising = True

    

    right_eye_points = cv2.convexHull(array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]))
    left_eye_points = cv2.convexHull(array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]))


    right_eye, h, w, x1, y1, w1, h1 = eyes_animations(frame, right_eye_points)
    right_eye, watch = animations(h, w, x1, y1, w1, h1, right_eye, eye_display)

    left_eye, h, w, x1, y1, w1, h1 = eyes_animations(frame, left_eye_points)
    left_eye, watch = animations(h, w, x1, y1, w1, h1, left_eye, eye_display)


    import numpy as np

    right_eye = cv2.resize(right_eye, (400, 350))
    left_eye = cv2.resize(left_eye, (400, 350))
    frame = cv2.resize(frame, (400, 350))

    image = cv2.imread(r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\display\eyes_model.jpg")
    image = cv2.resize(image, (400, 350))

    mask = np.zeros((350, 800 ,3), np.uint8)
    mask[0:, 0:] = 255, 255, 255

    

    analyse = ["dza", "njoi", "boiboibnoio"]
    x = 80
    y = 50

    cv2.putText(mask, "Watch to " + str(watch), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, 0)
    x = 80
    y = 100

    for i in range(len(analyse)):
        cv2.putText(mask, "Write context " + str(analyse[i]), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, 0)

        y += 50

    displaying1 = hstack((image, mask))


    

    displaying = hstack((right_eye, frame))
    displaying = hstack((displaying, left_eye))




    numpy_horizontal_concat = np.vstack( (displaying1, displaying) )

    cv2.imshow("aaa", numpy_horizontal_concat)
    cv2.waitKey(0)


    return raising
    

    








































