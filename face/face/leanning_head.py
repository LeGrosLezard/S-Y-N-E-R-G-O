def leaning_head(right_eye, left_eye, nose, head):
    """Calculus euclidian distance beetween eyes and nose,
    we calculus y coordiantes"""

    coeff = dist.euclidean(right_eye, nose) + dist.euclidean(left_eye, nose) 
    angle = int(250*(right_eye[1]-left_eye[1])/coeff)

    if angle < int(-0.15 * head[2]):print("penche gauche")
    elif angle > int(0.15 * head[2]):print("penche droite")
