def look_top_bot(ok, ok_haut, right_eye, left_eye, nose):
    """Calculus distance beetween nose and eyes line"""

    d_eyes = dist.euclidean(right_eye, left_eye) 
    d1 = dist.euclidean(right_eye, nose) 
    d2 = dist.euclidean(left_eye, nose) 

    coeff = d1 + d2

    cosb = np_min( (pow(d2, 2) - pow(d1, 2) + pow(d_eyes, 2) ) / (2*d2*d_eyes) )
    bent_up = int(250*(d2*sin(acos(cosb))-coeff/3.5)/coeff)


    if ok > 10 and bent_up >= 17: print("position baissé")

    elif bent_up >= 17:
        print("tete baissé")
        ok += 1

    elif ok_haut > 10 and bent_up <= -4: print("position levé")

    elif bent_up <= -4:
        print("tete levé")
        ok_haut += 1

    else:
        if ok_haut > 10: print("reprise position non levé")
        if ok > 10:print("reprise position non enfouis")
        ok = 0
        ok_haut = 0

    return ok, ok_haut
