import cv2
import shutil

from f_recuperate_informations_picture.hand_file.skeletton import hand_skelettor
from f_recuperate_informations_picture.hand_file.hand import treat_skeletton_points

from f_recuperate_informations_picture.fingers_file.fingers_analyse import fingers_analyse


def reading_picture(image):
    IM = image
    
    image = r"C:\Users\jeanbaptiste\Desktop\dougy_petits_pecs\a_images_to_read\a{}.jpg".format(str(IM))

    img = cv2.imread(image)
    copy_img = img.copy()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours = [sorted(cv2.findContours(gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0],
                                        key=cv2.contourArea)][0]

    copy = img.copy()
    rectangle = cv2.boundingRect(contours[-1])

    return copy_img, rectangle, img, image


def move_picture(sorted_fingers, path, image):

    path_ok_picture = r"C:\Users\jeanbaptiste\Desktop\dougy_petits_pecs\b_stock_image_5_pts\a{}.jpg".format(str(image))

    if len(sorted_fingers) == 5:
        shutil.move(path, path_ok_picture)


protoFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_deploy.prototxt"
weightsFile = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models\pose_iter_102000.caffemodel"

if __name__ == "__main__":


    image_reading = 1

    copy_img, rectangle, img, path = reading_picture(image_reading)


    points, position, finger = hand_skelettor(copy_img, protoFile, weightsFile)
    sorted_fingers = treat_skeletton_points(points, position, finger, rectangle, img)

    #move_picture(sorted_fingers, path, image_reading)


    fingers_analyse(sorted_fingers, img)
















