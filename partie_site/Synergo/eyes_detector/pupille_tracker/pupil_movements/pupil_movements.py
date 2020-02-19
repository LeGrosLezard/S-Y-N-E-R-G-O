def face_movement(landmarks, frame, eyes, head_box):


    joue = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in [2, 41, 31] ])),
            cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in [35, 14, 46] ])))


    #cv2.drawContours(frame, [joue[0]], -1, (0, 255, 0), 1)
    contour_right_joue = cv2.contourArea(joue[0])
    #cv2.drawContours(frame, [joue[1]], -1, (0, 255, 0), 1)
    contour_left_joue = cv2.contourArea(joue[1])

    eyeR_pts = landmarks.part(36).x, landmarks.part(36).y
    eyeL_pts = landmarks.part(45).x, landmarks.part(45).y
    noze_pts = landmarks.part(30).x, landmarks.part(30).y

    head1 = landmarks.part(2).x, landmarks.part(2).y
    head2 = landmarks.part(14).x, landmarks.part(14).y

    out = None
    out1 = None
    
    turning = turn_head(eyeR_pts, eyeL_pts, noze_pts, head_box)
    #print(turning)

    head_position = bent_up_head(eyeR_pts, eyeL_pts, noze_pts, head_box)
    #print("head position : ", head_position)

    if turning == "legerement a gauche":
        out = "gauche"
    elif turning == "legerement a droite":
        out =  "droite"

    if head_position == "position baissé":
        out1 = "bas"
    elif head_position == "position levé":
        out1 = "haut"

    return out, out1





TIMMER = []
POSITION_RIGHT = []
POSITION_LEFT = []
def eyes_movements(informations):

    frame, extremum, landmarks, head_box, eyes, glob, blanck, the_eye = informations


    nb = 0.42

    if the_eye == "right":


        xe, ye, we, he = extremum

        eye = [(j, i) for i in range(ye[1], he[1]) for j in range(xe[0], we[0])
               if frame[i, j][0] == 0 and frame[i, j][1] == 0 and frame[i, j][2] == 255]

        hauteur1 = [(j, i) for i in range(ye[1], he[1]) for j in range(xe[0], we[0])
                   if frame[i, j][0] == 255 and frame[i, j][1] == 255 and frame[i, j][2] == 255]

        hauteur2 = [(j, i) for i in range(ye[1], he[1]) for j in range(xe[0], we[0])
                   if frame[i, j][0] == 0 and frame[i, j][1] == 255 and frame[i, j][2] == 255]


        if eye != []:

            cv2.circle(blanck, eye[0], 1, (0, 255, 0), 1)

            cv2.circle(frame, eye[0], glob, (0, 255, 0), 1)

            total = int(dist.euclidean( (eyes[0][3][0][0], 0), (eyes[0][0][0][0], 0) ))

            gauche = dist.euclidean( (eyes[0][3][0][0], 0), (eye[0][0], 0) )

            droite = dist.euclidean( (eyes[0][0][0][0], 0), (eye[0][0], 0) )

            print(total, gauche, droite)
            if gauche <= int(total * nb):
                print("oeil gauche")
            elif droite <= int(total * nb):
                print("oeil droite")


            aa = landmarks.part(36).x, landmarks.part(36).y
            bb = landmarks.part(39).x, landmarks.part(39).y

            
            cc = int((aa[1] + bb[1])/2)

            mid_top = dist.euclidean((0, cc), (0, eye[0][1]))

            a = landmarks.part(41).x, landmarks.part(41).y
            b = landmarks.part(40).x, landmarks.part(40).y
            c = int((a[1] + b[1])/2)

            d = landmarks.part(37).x, landmarks.part(37).y
            e = landmarks.part(38).x, landmarks.part(38).y
            f = int((d[1] + e[1])/2)


            hauteur = dist.euclidean( (0, c), (0, f) )


            if mid_top >= int(hauteur * 0.34) and hauteur >= int(head_box[3] * 0.065):
                print("haut")

            elif hauteur <= int(head_box[3] *  0.036) and glob <= int(hauteur * 0.5):
                print("bas")



    if the_eye == "left":

        xe, ye, we, he = extremum

        eye = [(j, i) for i in range(ye[1], he[1]) for j in range(xe[0], we[0])
               if frame[i, j][0] == 0 and frame[i, j][1] == 0 and frame[i, j][2] == 255]



        if eye != []:

            cv2.circle(blanck, eye[0], 1, (0, 255, 0), 1)
            cv2.circle(frame, eye[0], glob, (0, 0, 255), 1)

            total = int(dist.euclidean( (eyes[1][3][0][0], 0), (eyes[1][0][0][0], 0) ))

            gauche = dist.euclidean( (eyes[1][3][0][0], 0), (eye[0][0], 0) )
            droite = dist.euclidean( (eyes[1][0][0][0], 0), (eye[0][0], 0) )

            print(total, gauche, droite)
            if gauche <= int(total * nb):
                print("oeil gauche")
            elif droite <= int(total * nb):
                print("oeil droite")



            aa = landmarks.part(42).x, landmarks.part(42).y
            bb = landmarks.part(45).x, landmarks.part(45).y

            cc = int((aa[1] + bb[1])/2)

            mid_top = dist.euclidean((0, cc), (0, eye[0][1]))

            a = landmarks.part(47).x, landmarks.part(47).y
            b = landmarks.part(46).x, landmarks.part(46).y
            c = int((a[1] + b[1])/2)

            d = landmarks.part(43).x, landmarks.part(43).y
            e = landmarks.part(44).x, landmarks.part(44).y
            f = int((d[1] + e[1])/2)


            hauteur = dist.euclidean( (0, c), (0, f) )


            if mid_top >= int(hauteur * 0.34) and hauteur >= int(head_box[3] * 0.065):
                print("haut")

            elif hauteur <= int(head_box[3] *  0.036) and glob <= int(hauteur * 0.5):
                print("bas")


