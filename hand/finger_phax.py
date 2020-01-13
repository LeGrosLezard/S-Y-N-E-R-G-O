import cv2


def phalange(pha, phax, pts1, pts2):

    if phax > 0:
        print("pahalange")
        print(phax)

    if 0 < phax < 10:
        print(pha + " pliée")

    elif phax > 0:
        direction_top = pts1[1] - pts2[1]

        if direction_top > 0:
            print(pha + " vers le haut")
        else:
            print(pha + " vers le bas")

        direction_bot = pts1[0] - pts2[0]

        if direction_bot > 5:
            print("vers droite")
        elif direction_bot < -5:
            print("vers gauche")
        else:
            print("droit")

    print("")

