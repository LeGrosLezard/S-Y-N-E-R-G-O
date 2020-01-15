import cv2
from scipy.spatial import distance as dist


def identify_fingers(thumb, fingers, crop, rectangle, direction, axis):

    print("")
    print("IDENTIFY FINGERS")

    print("Box de la main est de: ", rectangle)
    print(thumb)
    print(fingers)
    print(direction, axis)

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



    if direction in ("droite", "gauche"):
        area = "width"
    elif direction in ("bas", "haut"):
        area = "height"





    for i in points:
        if i != ():
            print(dist.euclidean(i, thumb[0][-1]))

    thumb_index = dist.euclidean(points[0], thumb[0][-1])
    print(thumb_index, (w,h))

    if area == "width" and thumb_index < w * 0.574 or\
       area == "height" and thumb_index < w * 0.574:
        draw(copy, fing[0], points[0])
        draw_line(copy, points[0], thumb[0][-1])
        fing.remove(fing[0])

    elif area == "width" and w * 0.775 > thumb_index > w * 0.574 or\
         area == "height" and w * 0.775 > thumb_index > w * 0.574:
        draw(copy, fing[1], points[0])
        draw_line(copy, points[0], thumb[0][-1])
        for i in range(2):
            fing.remove(fing[0])

    elif 130 > thumb_index > 105:
        draw(copy, fing[2], points[0])
        draw_line(copy, points[0], thumb[0][-1])
        fing.remove(fing[0])
        for i in range(3):
            fing.remove(fing[0])

    elif thumb_index > 130:
        draw(copy, fing[3], points[0])
        draw_line(copy, points[0], thumb[0][-1])
        for i in range(4):
            fing.remove(fing[0])


    cv2.imshow("thumb_next_finger", copy)
    cv2.waitKey(0)


    print("")

    for i in range(len(points)):

        print(fing)

        if i < len(points) - 1 and points[i] != () and points[i + 1] != ():


            a = dist.euclidean(points[i], points[i + 1])
            print(a, (w, h))


            #One point after
            if a < w * 0.295 and area == "width" or\
               a < w * 0.295 and area == "height":
                print("Moins 35")
                draw_line(copy, points[i], points[i + 1])
                draw(copy, fing[0], points[i + 1])
                fing.remove(fing[0])


            elif len(fing) == 1:
                print("reste plus qu'un doigt")
                draw_line(copy, points[i], points[i + 1])
                draw(copy, fing[0], points[i + 1])
                fing.remove(fing[0])


            elif (w * 0.295) * 2 > a > w * 0.295:
                print("1 doigt apres")
                draw_line(copy, points[i], points[i + 1])
                draw(copy, fing[1], points[i + 1])
                for i in range(2):
                    fing.remove(fing[0])


            elif (w * 0.295) * 3 > a > (w * 0.295) * 2:
                print("2 doigts apres")
                draw_line(copy, points[i], points[i + 1])
                draw(copy, fing[2], points[i + 1])
                for i in range(3):
                    fing.remove(fing[0])
                fing.remove(fing[0])

            elif (w * 0.295) * 4 > a > (w * 0.295) * 3:
                print("3 doigts apres")
                draw_line(copy, points[i], points[i + 1])
                draw(copy, fing[3], points[i + 1])
                for i in range(4):
                    fing.remove(fing[0])


            elif a > (w * 0.295) * 4:
                print("ici ecart supp a * 4")



            cv2.imshow("thumb_next_finger", copy)
            cv2.waitKey(0)
            print("")





    if len(fing) > 0: print("manque des doigts :", fing)



