import cv2
from numpy import array, hstack, zeros_like


def work_on_eye_picture(points, frame):

    def eyes_crop(eye, frame):
        x, y, w, h = cv2.boundingRect(eye)
        return frame[y-10:y+h, x:x+w], x, y, w, h

    def resizing(crop):
        height, width = crop.shape[:2]
        return cv2.resize(crop, (width*10, height*8))


    def bordering(crop, border_height, border_width):
      
        return cv2.copyMakeBorder(crop, top=border_height,bottom=border_height,
                                 left=border_width,right=border_width,
                                 borderType=cv2.BORDER_CONSTANT, value=[0, 0, 0])

    def difference_dimension(frame, crop):
        height, width = crop.shape[:2]
        height_frame, width_frame = frame.shape[:2]

        return int((height_frame - height) / 2), int((width_frame - width) / 2)


    crop, x, y, w, h = eyes_crop(points, frame)
    crop = resizing(crop)
    border_height, border_width = difference_dimension(frame, crop)
    crop = bordering(crop, border_height, border_width)

    return crop, border_height, border_width, x, y, w, h



def movement_eyes(eye_display):

    dico_movement = {"right":0, "left":0, "top":0, "bot":0}

    if eye_display != []:
        for i in eye_display:
            for k, v in dico_movement.items():
                if i == k:
                    dico_movement[k] += 1

    return dico_movement



def combinate_movements(dico_movement):
    movement = []
    for k, v in dico_movement.items():
        if dico_movement["right"] > 0 and dico_movement["top"] > 0: movement.append("droite haut")
        elif dico_movement["right"] > 0 and dico_movement["bot"] > 0: movement.append("droite bas")
        elif dico_movement["left"] > 0 and dico_movement["top"] > 0: movement.append("gauche haut")
        elif dico_movement["left"] > 0 and dico_movement["bot"] > 0: movement.append("gauche bas")
        elif dico_movement["right"] > 0: movement.append("droite")
        elif dico_movement["left"] > 0: movement.append("gauche")

    return movement

def situate_corner(height_difference, width_difference, x, y, w, h):

    corner_top = int((y+h) + height_difference - 90)
    center = int((y+h) + height_difference - 30)
    corner_bot = int((1+h) + height_difference + 30)

    return corner_top, center, corner_bot


def ajust_positions(h, w, corner_top, center, corner_bot):
    moves = {"droite":[(w, center), (w - 200, center), (w - 200 + 30, center + 30), (w - 200 + 30, center - 30)],
             "gauche":[(w + 140, center), (w + 340, center), (w + 340 - 30, center - 30), (w + 340 - 30, center + 30)],
             "droite haut":[(w, corner_top), (w - 100, corner_top - 100), (w - 100, corner_top - 100 + 30),(w - 100 + 30, corner_top - 100)],
             "droite bas":[(w, corner_bot), (w - 100, corner_bot + 100),(w - 100 + 30, corner_bot + 100),(w - 100, corner_bot + 100 - 30)],
             "gauche haut":[(w + 140, corner_top),(w + 240, corner_top - 100),(w + 240, corner_top - 100 + 30),(w + 240 - 30, corner_top - 100)],
             "gauche bas":[(w + 140, corner_bot), (w + 240, corner_bot + 100), (w + 240 - 30, corner_bot + 100),(w + 240, corner_bot + 100 - 30)]}

    return moves

def draw_lines(movement, moves, eye):

    watch = ""
    for i in movement:
        for k,v in moves.items():
            if i == k:
                cv2.line(eye, (v[0][0], v[0][1]), (v[1][0], v[1][1]), (0, 0, 255), 3)
                cv2.line(eye, (v[1][0], v[1][1]), (v[2][0], v[2][1]), (0, 0, 255), 3)
                cv2.line(eye, (v[1][0], v[1][1]), (v[3][0], v[3][1]), (0, 0, 255), 3)
                watch = k

    if watch == "":
        watch = "center"

    return watch, eye


def animations(h, w, x1, y1, w1, h1, eye, eye_display):
    """Eye display is the last movements from the eyes of personn"""
    
    dico_movement =  movement_eyes(eye_display)
    movement = combinate_movements(dico_movement)
    corner_top, center, corner_bot = situate_corner(h, w, x1, y1, w1, h1)
    moves = ajust_positions(h, w, corner_top, center, corner_bot)
    watch, eye = draw_lines(movement, moves, eye)

    return eye, watch





def eyes_display(frame, gray, landmarks, eyes_movements, eye_display, counter_frame):

    raising = False

    if eyes_movements != None:
        for i in eyes_movements:
            eye_display.append(i)

    if eye_display != [] and eyes_movements == None:
        raising = True


    right_eye_points = cv2.convexHull(array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]))
    left_eye_points = cv2.convexHull(array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]))

    right_crop, _, _, _, _, _,_  = work_on_eye_picture(right_eye_points, frame)
    left_crop, border_height, border_width, x, y, w, h = work_on_eye_picture(left_eye_points, frame)

    right_eye, _ = animations(border_height, border_width, x, y, w, h, right_crop, eye_display)
    left_eye, watch = animations(border_height, border_width, x, y, w, h, left_crop, eye_display)





















    import numpy as np

    right_eye = cv2.resize(right_eye, (400, 350))
    left_eye = cv2.resize(left_eye, (400, 350))
    frame = cv2.resize(frame, (400, 350))

    image = cv2.imread(r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\display\eyes_model.jpg")
    image = cv2.resize(image, (400, 350))

    mask = np.zeros((350, 800 ,3), np.uint8)
    mask[0:, 0:] = 255, 255, 255

    

    analyse = ["dza", "njoi", "boiboibnoio"]
    x = 80
    y = 50

    cv2.putText(mask, "Watch to " + str(watch), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, 0)
    x = 80
    y = 100

    for i in range(len(analyse)):
        cv2.putText(mask, "Write context " + str(analyse[i]), (x, y), cv2.FONT_HERSHEY_PLAIN, 1, 0)

        y += 50

    displaying1 = hstack((image, mask))
    displaying = hstack((right_eye, frame))
    displaying = hstack((displaying, left_eye))

    numpy_horizontal_concat = np.vstack( (displaying1, displaying) )

    cv2.imshow("aaa", numpy_horizontal_concat)
    cv2.waitKey(0)


    return raising
    

    








































