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
            if x == 0: x = width_phax[-1]

            drawing_width(copy, points[i], points[i + 1], x)

            sens = ""

            if x > 0  : sens += "droite"                    #Choice his direction
            elif x < 0: sens += "gauche"   
            elif x == 0: sens += sens_phax[-1]
            if y > 0  : sens += " bas"   
            elif y < 0: sens += " haut"   


            sens_phax.append(sens)                          #Append width, direction phax.
            width_phax.append(abs(x))

    for i in range(3 - len(width_phax)):
        width_phax.append(None)

    for i in range(3 - len(sens_phax)):
        sens_phax.append(None)

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

    fingers_dico = {'thumb': [(97, 105), (115, 94), (122, 79), (126, 69)], 'I': [(86, 76), (83, 55), (83, 47), (83, 40)], 'M': [(75, 79), (68, 55)], 'An': [], 'a': [(51, 98), (44, 91), (40, 94), (41, 90)]}
    image = r"C:\Users\jeanbaptiste\Desktop\dougy_petits_pecs\a_images_to_read\{}.jpg".format("a")
    img = cv2.imread(image)

    sens_phax, width_phax = finger_phax_sens_width(fingers_dico, img)
    print(sens_phax, "\n", width_phax)

















