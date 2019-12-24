def look_right_left(right_eye, left_eye, nose):
    """Calculus difference beetween left right distance"""

    d1 = dist.euclidean(right_eye, nose) 
    d2 = dist.euclidean(left_eye, nose)
    coeff = d1 + d2

    look_to = int(250*(d1-d2)/coeff)

    if coeff > 95:
        if look_to < -0.50 * coeff : print("tourne a droite")
        elif look_to > 0.50 * coeff : print("tourne a gauche")
    else:
        if look_to < -0.55 * coeff : print("tourne a droite")
        elif look_to > 0.55 * coeff : print("tourne a gauche")
