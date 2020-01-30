import math

(75, 79), (68, 55)

from scipy.spatial import distance as dist
from ok1 import *


def rat(ratio1, ratio2):
    a = False
    if ratio1 > ratio2:
        #print("error")
        a = True
    ratio = ratio2 / ratio1

    return ratio, a

a = math.degrees(math.atan(79-55/68-75))
#y1-y2/x2-x1
print(a)

b = dist.euclidean((75, 79), (68, 55))
print(b)


x = int(b * math.cos(a))
y = int(b * math.sin(a))


print(x, y)




distance = []
angle = []
dat = []
for csv_name in range(1, 8):
    data_csv = recuperate_data_in_csv(csv_name)

    for nb, data in enumerate(data_csv):
        dataa, ratio = data[0], data[1]

        data = points_to_fingers_dict(dataa)

        x1, y1 = data["m"][0][0][0], data["m"][0][0][1]
        x2, y2 = data["m"][1][0][0], data["m"][1][0][1]

        
        e = dist.euclidean((x1, y1), (x2, y2))


        d = math.degrees(math.atan(y2-y1/x1-x2))

        distance.append(e)
        angle.append(d)
        dat.append((dataa, ratio[2] * ratio[3]))


kk = []
for nb, (i, j) in enumerate(zip(distance, angle)):
    #print(nb, i, j)


    ratio, er = rat(113 * 109, dat[nb][1])

    if er is True:
        b = b / ratio
    else:
        i = i / ratio



    yoyo = math.sqrt((a - j)**2 + (b - i)**2)

    if nb == 41:
        print(ratio)
    kk.append((yoyo, nb))
#x currnet - x, y current - y)






aaaaa = sorted(kk, key=lambda x: x[0])
print(aaaaa)


print("MAINTENANT PRENDRE LE DOIGT ENTIER PTETRE CHAI PAS ON VERRA")



blank_image = np.zeros((500, 500, 3), np.uint8)
for i in dat[41][0]:
    for j in i:

        cv2.circle(blank_image, (int(j[0]), int(j[1])) , 2, (0, 0, 255), 2)
        cv2.line(blank_image, (i[0]), (i[1]), (0, 255, 0), 2)

        cv2.circle(blank_image, (75, 79) , 2, (0, 0, 255), 2)
        cv2.circle(blank_image,(68, 55) , 2, (0, 0, 255), 2)
        cv2.line(blank_image, (75, 79), (68, 55), (0, 255, 0), 2)


cv2.imshow("blank_imageaaa", blank_image)
cv2.waitKey(0)









