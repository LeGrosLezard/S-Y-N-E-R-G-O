import cv2
from scipy.spatial import distance as dist


def identify_fingers(thumb, fingers, crop, rectangle, direction):
    print("")
    print("IDENTIFY FINGERS")

    print("Box de la main est de: ", rectangle)
    print(thumb)
    print(fingers)
    print(direction)

    copy = crop.copy()



    [cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
    [cv2.circle(copy, j, 2, (0, 0, 255), 2) for i in fingers for j in i[0]]


    fingers += [None for i in range(4 - len(fingers))]
    points = [(lambda x: () if x == None else x[0][-1])(i) for i in fingers]


    font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    draw = lambda picture, text, pts:\
        cv2.putText(copy, text, pts, font, 1, (255, 255, 255), 1, cv2.LINE_AA)


    draw_line = lambda picture, pts1, pts2:\
        cv2.line(picture, pts1, pts2, (0, 255, 0), 1)




    cv2.circle(copy, thumb[0][-1], 2, (255, 255, 255), 2)
    draw(copy, "P", thumb[0][-1])



    fing = ["I", "M", "An", "a"]


    x, y, w, h = rectangle
    print(w, h)

    if direction in ("droite", "gauche"):
        area = "width"
    elif direction in ("bas", "haut"):
        area = "height"


    thumb_index = dist.euclidean(points[0], thumb[0][-1])

    print(thumb_index)
    if area == "width" and thumb_index < w * 0.535 or\
       area == "height" and thumb_index < w * 0.535:
        draw(copy, fing[0], points[0])
        draw_line(copy, points[0], thumb[0][-1])
        fing.remove(fing[0])

    elif 100 > thumb_index > 74:
        draw(copy, fing[1], points[0])
        draw_line(copy, points[1], thumb[0][-1])
        for i in range(2):
            fing.remove(fing[0])

    elif 130 > thumb_index > 100:
        draw(copy, fing[2], points[0])
        draw_line(copy, points[2], thumb[0][-1])
        fing.remove(fing[0])
        for i in range(2):
            fing.remove(fing[3])

    elif thumb_index > 130:
        draw(copy, fing[3], points[0])
        draw_line(copy, points[3], thumb[0][-1])
        for i in range(4):
            fing.remove(fing[0])


    cv2.imshow("thumb_next_finger", copy)
    cv2.waitKey(0)




    print(points)

    for i in range(len(points)):

        if i < len(points) - 1:

            print(points[i], points[i + 1])


            a = dist.euclidean(points[i], points[i + 1])
            print(a)



            if a < 35:  #One point after
                print("Moins 35")
                draw_line(copy, points[i], points[i + 1])
                draw(copy, fing[0], points[i + 1])
                fing.remove(fing[0])


            if a > 74 and a < 100:  #Two point after

                print("74 - 100")
                draw_line(copy, points[i], points[i + 1])
                draw(copy, fing[1], points[i + 1])

                for i in range(2):
                    fing.remove(fing[0])
                


            cv2.imshow("thumb_next_finger", copy)
            cv2.waitKey(0)
            print("")





