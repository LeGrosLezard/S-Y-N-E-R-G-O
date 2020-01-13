import cv2
import numpy as np
from scipy.spatial import distance as dist


rectangle=(35, 41, 104, 86)
mid = 69, 63
skeletton=[[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], [0, 9], [9, 10], [10, 11], [11, 12], [0, 13], [13, 14], [14, 15], [15, 16], [0, 17], [17, 18], [18, 19], [19, 20]]


finger=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]


position=[((87, 106), (101, 95)), ((101, 95), (115, 88)), ((115, 88), (123, 80)), ((123, 80), (130, 69)), ((87, 106), (84, 74)), ((84, 74), (80, 59)), ((80, 59), (76, 55)), ((76, 55), (73, 51)), ((87, 106), (73, 81)), ((73, 81), (62, 66)), ((62, 66), (55, 66)), ((55, 66), (48, 69)), ((87, 106), (65, 91)), ((65, 91), (55, 81)), ((55, 81), (51, 77)), ((51, 77), (44, 77)), ((87, 106), (58, 102)), ((58, 102), (44, 95)), ((44, 95), (40, 95)), ((40, 95), (37, 92))]
thumb = [((101, 95), (115, 88)), ((115, 88), (123, 80)), ((123, 80), (130, 69))]
index =[((84, 74), (80, 59)), ((80, 59), (76, 55)), ((76, 55), (73, 51))]
major = [((73, 81), (62, 66)), ((62, 66), (55, 66)), ((55, 66), (48, 69))]
annular =[((65, 91), (55, 81)), ((55, 81), (51, 77)), ((51, 77), (44, 77))]
auricular = [((58, 102), (44, 95)), ((44, 95), (40, 95)), ((40, 95), (37, 92))]
palm = [[position[5][0], position[9][0], position[13][0],
        position[17][0], position[0][0], position[0][1], position[1][1]],
        [position[5][0], position[9][0], position[13][0],
        position[17][0], position[1][1], position[0][1], position[0][0]]]

(32, 137, 133, 118, 88)
sort = [32, 88, 118, 133, 137]

finger = [[((65, 112), (50, 101)), ((50, 101), (39, 90)), ((39, 90), (32, 85))],
 [((99, 112), (118, 112)), ((118, 112), (126, 112)), ((126, 112), (137, 112))],
 [((95, 97), (111, 82)), ((111, 82), (122, 74)), ((122, 74), (133, 66))],
 [((84, 89), (100, 70)), ((100, 70), (110, 59)), ((110, 59), (118, 47))],
 [((76, 82), (81, 66)), ((81, 66), (84, 55)), ((84, 55), (88, 44))]]





fingers = [[((0, 0), (0, 0)), ((119, 82), (127, 80)), ((127, 80), (137, 77))], [((59, 67), (44, 61)), ((44, 61), (44, 62)), ((44, 62), (41, 62))], [((57, 77), (47, 80)), ((47, 80), (37, 82)), ((37, 82), (29, 85))], [((59, 89), (46, 93)), ((46, 93), (39, 95)), ((39, 95), (31, 97))], [((62, 98), (51, 100)), ((0, 0), (0, 0)), ((0, 0), (0, 0))]]


IM = 27


image = r"C:\Users\jeanbaptiste\Desktop\hand_picture\a{}.jpg".format(str(IM))
crop = cv2.imread(image)

copy = crop.copy()


thumb = [[(62, 80), (48, 78), (33, 72), (25, 67)], 'gauche']

fingers = [[[(83, 38), (89, 30)], 'droite'],
           [[(84, 64), (104, 46), (115, 41), (123, 35)], 'droite'],
           [[(99, 88), (118, 91), (139, 102)], 'droite']]



[cv2.circle(copy, i, 2, (0, 0, 0), 2) for i in thumb[0]]
[cv2.circle(copy, j, 2, (0, 0, 255), 2) for i in fingers for j in i[0]]


fingers += [None for i in range(4 - len(fingers))]
points = [(lambda x: () if x == None else x[0][-1])(i) for i in fingers]



font = cv2.FONT_HERSHEY_COMPLEX_SMALL

cv2.circle(copy, thumb[0][-1], 2, (255, 255, 255), 2)
cv2.putText(copy, 'P', thumb[0][-1], font,  
                        1, (255, 255, 255), 1, cv2.LINE_AA)

fing = ["I", "M", "An", "a"]


for i in range(len(points)):

    if i == 0:
        print(thumb[0][-1], points[i])
        cv2.line(copy, (points[i]), (thumb[0][-1]), (0, 255, 0), 1)
        a = dist.euclidean(points[i], thumb[0][-1])
        print(a)

        cv2.line(copy, (points[0]), (thumb[0][-1]), (0, 255, 0), 1)
        a = dist.euclidean(points[0], thumb[0][-1])
        if a < 74:
           
            cv2.putText(copy, fing[i], points[0], font,  
                        1, (255, 255, 255), 1, cv2.LINE_AA)
        if a > 75 and a < 100:
            cv2.putText(copy, fing[i + 1], points[0], font,  
                        1, (255, 255, 255), 1, cv2.LINE_AA)

        elif a > 100 and a < 130:
            cv2.putText(copy, fing[i + 2], points[0], font,  
                        1, (255, 255, 255), 1, cv2.LINE_AA)

        elif a > 130:
            cv2.putText(copy, fing[i + 3], points[0], font,  
                        1, (255, 255, 255), 1, cv2.LINE_AA)

        cv2.imshow("thumb", copy)
        cv2.waitKey(0)


        print("")



    if i < len(points) - 1:

        print(points[i], points[i + 1])
        if points[i] is not () and points[i + 1] is not ():
            cv2.line(copy, (points[i]), (points[i + 1]), (0, 255, 0), 1)
            a = dist.euclidean(points[i], points[i + 1])
            print(a)



            if a < 35:
                
                cv2.putText(copy, fing[i + 1], points[i + 1], font,  
                            1, (255, 255, 255), 1, cv2.LINE_AA)

            elif a > 35 and a < 70:
                print("plus que 35 next points")
                cv2.putText(copy, fing[i + 2], points[i + 1], font,  
                            1, (255, 255, 255), 1, cv2.LINE_AA)


            elif a > 70 and a < 105:
                print("plus que 35 next points")
                cv2.putText(copy, fing[i + 3], points[i + 1], font,  
                            1, (255, 255, 255), 1, cv2.LINE_AA)

            elif a > 105:
                cv2.putText(copy, fing[i + 4], points[i + 1], font,  
                            1, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.imshow("thumb", copy)
            cv2.waitKey(0)
            print("")


    print("")






























