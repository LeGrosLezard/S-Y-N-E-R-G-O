def doigts_plié(points, crop):

    copy = crop.copy()

    cv2.line(copy, points[0], points[1], (0, 0, 255), 2)
    cv2.line(copy, points[1], points[3], (0, 0, 255), 2)
    cv2.line(copy, points[3], points[0], (0, 0, 255), 2)
    #0 1 3 -> phalange


    #pts 3 > pts1
    if points[3][1] + 5 >= points[1][1]:
        print("doigt plié vers le bas")

    #pts3 LEFT pts0; pts3 > pts1
    if points[0][0] >= points[3][0] and points[3][1] + 5 >= points[1][1]:
        print("plié vers droit")

    #pts3 RIGHT pts0; pts3 > pts1
    if points[0][0] <= points[3][0] and points[3][1] + 5 >= points[1][1]:
        print("plié vers gauche") 

    #pts0 LEFT pts3; pts3 > pts1; (pts3 - pts0) < 15
    if points[0][0] >= points[3][0] and points[3][1] + 5 >= points[1][1] and\
       abs(points[3][1] - points[0][1]) <= 15:
        print("plié vers droit")
 
    if points[0][0] <= points[3][0] and points[3][1] + 5 >= points[1][1] and\
       abs(points[3][1] - points[0][1]) <= 15:
        print("plié vers gauche") 


    cv2.imshow("angle doigt plié", copy)
    cv2.waitKey(0)
