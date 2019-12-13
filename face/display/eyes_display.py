import cv2
from numpy import array, hstack, zeros_like

def eyes_display(frame, gray, landmarks, eyes_movements):

    right_eye_points = cv2.convexHull(array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]))
    left_eye_points = cv2.convexHull(array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]))

    copy = frame.copy()



    x1, y1, w1, h1 = cv2.boundingRect(right_eye_points)
    right_crop = frame[y1-10:y1+h1, x1:x1+w1]



    x2, y2, w2, h2 = cv2.boundingRect(left_eye_points)
    left_crop = frame[y2-10:y2+h2, x2:x2+w2]





    height, width = right_crop.shape[:2]
    right_eye = cv2.resize(right_crop, (width*10, height*8))
    left_eye = cv2.resize(left_crop, (width*10, height*8))

    height_f, width_f = frame.shape[:2]

    h = int((height_f - height) / 2)
    w = int((width_f - width) / 2)













    right_eye = cv2.copyMakeBorder(right_eye,
                                    top=h,bottom=h,left=w,right=w,
                                    borderType=cv2.BORDER_CONSTANT,
                                    value=[0, 0, 0])

    a = int(((y1+h1)) + h - 30)
    
    cv2.circle(right_eye, (w, a), 3, (255, 255, 255), 3)
    cv2.circle(right_eye, (w + 140, a), 3, (255, 255, 255), 3)


    aa = int(((y1+h1)) + h - 90)
    cv2.circle(right_eye, (w, aa), 3, (0, 0, 255), 3)
    cv2.circle(right_eye, (w + 140, aa), 3, (0, 0, 255), 3)


    aaa = int(((y1+h1)) + h + 30)
    cv2.circle(right_eye, (w, aaa), 3, (255, 0, 0), 3)
    cv2.circle(right_eye, (w + 140, aaa), 3, (255, 0, 0), 3)

    moves = {"droite":[(w, a), (w - 200, a), (w - 200 + 30, a + 30), (w - 200 + 30, a - 30)],
             "droite haut":[(w, aa), (w - 100, aa - 100), (w - 100, aa - 100 + 30), (w - 100 + 30, aa - 100)],
             "droite bas":[(w, aaa), (w - 100, aaa + 100), (w - 100 + 30, aaa + 100), (w - 100, aaa + 100 - 30)],
             "gauche":[(w + 140, a), (w + 340, a), (w + 340 - 30, a - 30), (w + 340 - 30, a + 30)],
             "gauche haut":[(w + 140, aa), (w + 240, aa - 100), (w + 240, aa - 100 + 30), (w + 240 - 30, aa - 100)],
             "gauche bas":[(w + 140, aaa), (w + 240, aaa + 100), (w + 240 - 30, aaa + 100), (w + 240, aaa + 100 - 30)]}



    for k,v in moves.items():
        cv2.line(right_eye, (v[0][0], v[0][1]), (v[1][0], v[1][1]), (255, 255, 255), 3)
        try:
            cv2.line(right_eye, (v[1][0], v[1][1]), (v[2][0], v[2][1]), (255, 255, 255), 3)
            cv2.line(right_eye, (v[1][0], v[1][1]), (v[3][0], v[3][1]), (255, 255, 255), 3)

        except:
            pass





    if eyes_movements != None:
        for i in eyes_movements:
            for k,v in moves.items():
                if i == k:
                    pass











    left_eye = cv2.copyMakeBorder(left_eye,
                                  top=h,bottom=h,left=w, right=w,
                                  borderType=cv2.BORDER_CONSTANT,
                                  value=[0, 0, 0])


    a = int(((y1+h1)) + h - 30)
    
    cv2.circle(left_eye, (w, a), 3, (0, 255, 255), 3)
    cv2.circle(left_eye, (w + 140, a), 3, (0, 255, 255), 3)


    aa = int(((y1+h1)) + h - 90)
    cv2.circle(left_eye, (w, aa), 3, (0, 0, 255), 3)
    cv2.circle(left_eye, (w + 140, aa), 3, (0, 0, 255), 3)


    aaa = int(((y1+h1)) + h + 30)
    cv2.circle(left_eye, (w, aaa), 3, (255, 0, 0), 3)
    cv2.circle(left_eye, (w + 140, aaa), 3, (255, 0, 0), 3)





    moves = {"droite":[(w, a), (w - 200, a), (w - 200 + 30, a + 30), (w - 200 + 30, a - 30)],
             "droite haut":[(w, aa), (w - 100, aa - 100), (w - 100, aa - 100 + 30), (w - 100 + 30, aa - 100)],
             "droite bas":[(w, aaa), (w - 100, aaa + 100), (w - 100 + 30, aaa + 100), (w - 100, aaa + 100 - 30)],
             "gauche":[(w + 140, a), (w + 340, a), (w + 340 - 30, a - 30), (w + 340 - 30, a + 30)],
             "gauche haut":[(w + 140, aa), (w + 240, aa - 100), (w + 240, aa - 100 + 30), (w + 240 - 30, aa - 100)],
             "gauche bas":[(w + 140, aaa), (w + 240, aaa + 100), (w + 240 - 30, aaa + 100), (w + 240, aaa + 100 - 30)]}



    for k,v in moves.items():
        cv2.line(left_eye, (v[0][0], v[0][1]), (v[1][0], v[1][1]), (255, 255, 255), 3)
        try:
            cv2.line(left_eye, (v[1][0], v[1][1]), (v[2][0], v[2][1]), (255, 255, 255), 3)
            cv2.line(left_eye, (v[1][0], v[1][1]), (v[3][0], v[3][1]), (255, 255, 255), 3)

        except:
            pass





    right_eye = cv2.resize(right_eye, (400, 350))
    left_eye = cv2.resize(left_eye, (400, 350))
    frame = cv2.resize(frame, (400, 350))



    


    











    displaying = hstack((right_eye, frame))
    displaying = hstack((displaying, left_eye))

    cv2.imshow("displaying", displaying)
    cv2.waitKey(0)


























