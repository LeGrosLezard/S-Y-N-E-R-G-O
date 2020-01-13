def analyse_space_thumb_fingers(finger, finger2, palm, crop):

    copy = crop.copy()


    print(finger)
    print(finger2)

    cv2.line(copy, palm, finger[-1][1], (0,255,255), 1)
    cv2.line(copy, finger[-1][1], finger2[-1][1], (0,255,255), 1)
    cv2.line(copy, finger2[-1][1], palm, (0,255,255), 1)


    cv2.circle(copy, palm, 2, (255, 255, 255), 2)
    cv2.circle(copy, finger[-1][1], 2, (255, 255, 255), 2)
    cv2.circle(copy, finger2[-1][1], 2, (255, 255, 255), 2)


    bc = dist.euclidean(finger[-1][1], finger2[-1][1])
    ca = dist.euclidean(finger2[-1][1], palm)
    print(ab, bc, ca)

    font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    cv2.putText(copy, 'A', palm, font,  
                       1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(copy, 'B', finger[-1][1], font,  
                       1, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(copy, 'C', finger2[-1][1], font,  
                       1, (255, 255, 255), 1, cv2.LINE_AA)



    #pouce plus haut qu'index
    if finger[-1][1][1] + 5 < finger2[-1][1][1]:
        print("iciiiiiiiiiii a faire")



    #pouce plus bas index
    elif finger2[-1][1][1] + 5 > finger2[-1][1][1]:

        cb_2 = (ca**2) + (ab**2) - (bc**2)
        cos = (2 * ca * ab)
        angle = math.degrees(math.acos(cb_2 / cos))
        print(angle)




    cv2.imshow("analyse space", copy)
    cv2.waitKey(0)
