from cv2 import bitwise_and, polylines, fillConvexPoly, imshow, imread, resize, cvtColor, COLOR_BGR2GRAY, line
from numpy import zeros_like, hstack, empty, uint8

#en gros on veut un affichage a la iron man


#on récupere la gueule une neutre, l'autre avec les triangle, et
#l'autre avec l'objet



#on l'aggrandit

#si touché -> c pas dans display

#mettre la zone en bleu
#définir un nom de zone (ex: joue par droite + nombre de frame a la fin)
#l'afficher

def displaying(gray, img, copy, convexhull):

    head_model = imread("head_model.jpg")
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



















