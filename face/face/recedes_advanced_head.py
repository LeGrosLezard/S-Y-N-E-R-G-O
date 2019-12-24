def movements_dude(landmarks, points_position):

    pointsA = [0, 1, 2]
    pointsB = [16, 15, 14]

    out = False
    for i in range(len(pointsA)):
        a = landmarks.part(pointsA[i]).x
        b = landmarks.part(pointsB[i]).x
        c = (b-a)

        if c < np.mean(points_position[i]) - 6:
            print("recule")
            out = True
 
        elif c > np.mean(points_position[i]) + 7:
            print("s'avance")
            out = True

        points_position[i].append(c)

    return out
