from cv2 import bitwise_and, polylines, fillConvexPoly, imshow, imread, resize, cvtColor, COLOR_BGR2GRAY, line
from numpy import zeros_like, hstack, empty, uint8


#si touché -> c pas dans display

#mettre la zone en bleu
#définir un nom de zone (ex: joue par droite + nombre de frame a la fin)
#l'afficher


def displaying(gray, img, copy, convexhull):

    head_model = imread("display/head_model.jpg")
    head_model = resize(head_model, (int(gray.shape[1]/2), gray.shape[0]))

    mask = zeros_like(gray)

    polylines(copy, [convexhull], True, (0, 0, 255), 1)
    fillConvexPoly(mask, convexhull, 255)

    face = bitwise_and(copy, copy, mask=mask)

    displaying = hstack((head_model, img))
    displaying = hstack((displaying, face))

    imshow('Display', displaying)


def recuperate_face(convexhull, gray, img, points):
    """We displaying the frame, the face
    from the frame"""

    copy = img.copy()

    for pts in points:
        pts1 = pts[0]; pts2 = pts[1]; pts3 = pts[2]

        line(copy, pts1, pts2, (0, 0, 255), 1)
        line(copy, pts2, pts3, (0, 0, 255), 1)
        line(copy, pts1, pts3, (0, 0, 255), 1)

    displaying(gray, img, copy, convexhull)






##def make_rectangle(area, color):
##    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for pts in face for n in range(area[0], area[1])])
##    x, y, w, h = boundingRect(area)
##    cv2.rectangle(img, (x, y), (x + w, y + h), color, 1) 
##    return x, y, w, h
##
##def make_contour(area, color):
##    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for pts in face for n in area])
##    cv2.drawContours(img, [area], 0, color, 1)
##
##
##areas =  { "beet_eyes" :[21, 22, 27], "chin":[58, 56, 9, 7], "chin1":[58, 7, 3, 48],
##           "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 0, 28],
##           "cheek2":[54, 13, 16, 28], "noze_area":[27, 48, 54], "mouse":(48, 61),
##           "onEye1":(17, 22), "onEye2":(22, 27), "leftEye":(36, 42), "rightEye":(42, 48)}
##
##[make_contour(areas[k], (0,255,0)) for nb, k in enumerate(areas) if nb <= 6]
##[make_rectangle(areas[k], (0,255,0)) for nb, k in enumerate(areas) if nb > 6]
##











