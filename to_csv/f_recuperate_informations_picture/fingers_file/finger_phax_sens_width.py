import cv2


def drawing_width(copy, pts1, pts2, width_tickness):

    cv2.circle(copy, pts1, 2, (0, 0, 255), 2)
    cv2.circle(copy, pts2, 2, (0, 255, 0), 2)

    cv2.line(copy, pts1, pts2, (255, 255, 255), abs(width_tickness))

    cv2.imshow("dszhgdf", copy)
    cv2.waitKey(0)



def phalange_sens_width(name, points, copy):

    sens_phax = []                                          #Direction of each phax
    width_phax = []                                         #Width phax


    for i in range(len(points)):                            #Run points (phaxs)
        if i < len(points) - 1:

            x = points[i + 1][0] - points[i][0]             #X axis
            y = points[i + 1][1] - points[i][1]             #Y axis

            drawing_width(copy, points[i], points[i + 1], x)

            sens = ""

            if x > 0  : sens += "droite"                    #Choice his direction
            elif x < 0: sens += "gauche"   
            if y > 0  : sens += " bas"   
            elif y < 0: sens += " haut"   


            sens_phax.append(sens)                          #Append width, direction phax.
            width_phax.append(abs(x))


    width_phax.append(name)

    print(sens_phax)
    print(width_phax)

    return sens_phax, width_phax




def finger_phax_sens_width(fingers_dico, crop):

    copy = crop.copy()

    sens_phax = []
    width_phax = []

    for k, v in fingers_dico.items():
        print(k)
        sens, width = phalange_sens_width(k, v, copy)

        sens_phax.append(sens)
        width_phax.append(width)
        print("")

    return sens_phax, width_phax



if __name__ == "__main__":

    fingers_dico = {'thumb': [(102, 97), (113, 89), (123, 79), (131, 68)], 'I': [(85, 72), (81, 57), (78, 50), (75, 44)], 'M': [(74, 79), (61, 65), (54, 64), (47, 62)], 'An': [(64, 89), (57, 82), (50, 75), (46, 71)], 'a': [(61, 104), (50, 100), (43, 96), (36, 93)]}
    image = r"C:\Users\jeanbaptiste\Desktop\dougy_petits_pecs\a_images_to_read\a{}.jpg".format(str(1))
    img = cv2.imread(image)

    sens_phax, width_phax = finger_phax_sens_width(fingers_dico, img)
    print(sens_phax, "\n", width_phax)
















