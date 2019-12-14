from cv2 import boundingRect, resize, BORDER_CONSTANT, copyMakeBorder, line, FONT_HERSHEY_PLAIN, imread, putText, convexHull, imshow
from numpy import array, hstack, zeros_like, zeros, uint8, vstack


def eyes_crop(eye, frame):
    """Recuperate area of the frame interest."""
    x, y, w, h = boundingRect(eye)
    return frame[y-10:y+h, x:x+w], x, y, w, h

def resizing(crop):
    """Resize the crop (*10;*8)"""
    height, width = crop.shape[:2]
    return resize(crop, (width*10, height*8))

def difference_dimension(frame, crop):
    """Recuperate difference beetween frame and the crop dimensions.
    Because we need the same sizes for stack them."""
    height, width = crop.shape[:2]
    height_frame, width_frame = frame.shape[:2]
    return int((height_frame - height) / 2), int((width_frame - width) / 2)

def bordering(crop, border_height, border_width):
    """Make balck borders of the mask."""
    return copyMakeBorder(crop, top=border_height,bottom=border_height,
                          left=border_width,right=border_width,
                          borderType=BORDER_CONSTANT, value=[0, 0, 0])


def work_on_eye_picture(points, frame):
    """We treat the crop eyes"""

    crop, x, y, w, h = eyes_crop(points, frame)
    crop = resizing(crop)
    border_height, border_width = difference_dimension(frame, crop)
    crop = bordering(crop, border_height, border_width)

    return crop, border_height, border_width, x, y, w, h





def combinate_movements(eye_display):
    """From the last frame we recuperate eyes movements and combinate
    them"""
    movement = []
    if "right" in eye_display and "top" in eye_display: movement.append("droite haut")
    elif "right" in eye_display and "bot" in eye_display: movement.append("droite bas")
    elif "left" in eye_display and "top" in eye_display: movement.append("gauche haut")
    elif "left" in eye_display and "bot" in eye_display: movement.append("gauche bas")
    elif "right" in eye_display: movement.append("droite")
    elif "left" in eye_display: movement.append("gauche")
    elif "right" in eye_display and "left" in eye_display: movement.append("don")
    return movement

def situate_corner(height_difference, width_difference, x, y, w, h):
    """Find corner of the mask for draw the arrows"""
    return int( (y+h) + height_difference - 90),\
           int( (y+h) + height_difference - 30),\
           int( (1+h) + height_difference + 30)

def ajust_positions(h, w, corner_top, center, corner_bot):
    """Ajust position of arrow in function of the size of the crop"""
    return { "droite":[(w, center), (w - 200, center), (w - 200 + 30, center + 30), (w - 200 + 30, center - 30)],
             "gauche":[(w + 140, center), (w + 340, center), (w + 340 - 30, center - 30), (w + 340 - 30, center + 30)],
             "droite haut":[(w, corner_top), (w - 100, corner_top - 100), (w - 100, corner_top - 100 + 30),(w - 100 + 30, corner_top - 100)],
             "droite bas":[(w, corner_bot), (w - 100, corner_bot + 100),(w - 100 + 30, corner_bot + 100),(w - 100, corner_bot + 100 - 30)],
             "gauche haut":[(w + 140, corner_top),(w + 240, corner_top - 100),(w + 240, corner_top - 100 + 30),(w + 240 - 30, corner_top - 100)],
             "gauche bas":[(w + 140, corner_bot), (w + 240, corner_bot + 100), (w + 240 - 30, corner_bot + 100),(w + 240, corner_bot + 100 - 30)]
           }

def draw_lines(movement, moves, eye):
    """Draw lines"""
    watch = ""
    for i in movement:
        for k, v in moves.items():
            if i == k:
                line(eye, (v[0][0], v[0][1]), (v[1][0], v[1][1]), (0, 0, 255), 3)
                line(eye, (v[1][0], v[1][1]), (v[2][0], v[2][1]), (0, 0, 255), 3)
                line(eye, (v[1][0], v[1][1]), (v[3][0], v[3][1]), (0, 0, 255), 3)
                watch = k

    if watch == "":
        watch = "center"

    return watch, eye

def animations(h, w, x1, y1, w1, h1, eye, eye_display):
    """Eye display is the last movements from the eyes of personn"""

    movement = combinate_movements(eye_display)
    corner_top, center, corner_bot = situate_corner(h, w, x1, y1, w1, h1)
    moves = ajust_positions(h, w, corner_top, center, corner_bot)
    watch, eye = draw_lines(movement, moves, eye)

    return eye, watch





def part_analyse(analyse, watch):
    """Recuperate in function of the movement the picture path"""
    font = FONT_HERSHEY_PLAIN; x = 80; y = 100
    path = {"center" : r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\display\eyes_pictures\0.jpg",
            "droite haut" : r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\display\eyes_pictures\1.jpg",
            "droite" : r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\display\eyes_pictures\2.jpg",
            "droite bas" : r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\display\eyes_pictures\3.jpg",
            "gauche haut" : r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\display\eyes_pictures\4.jpg",
            "gauche" : r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\display\eyes_pictures\5.jpg",
            "gauche bas" : r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\display\eyes_pictures\6.jpg"}

    image = imread(path[watch])
    image = resize(image, (400, 350))

    mask = zeros((350, 800 ,3), uint8)
    mask[0:, 0:] = 255, 255, 255

    putText(mask, "Watch to " + str(watch), (80, 50), font, 1, 0)

    for i in range(len(analyse)):
        putText(mask, "Write context " + str(analyse[i]), (x, y), FONT_HERSHEY_PLAIN, 1, 0)
        y += 50

    return hstack((image, mask))


def part_video(frame, right_eye, left_eye):
    """Resize crops and frame for stack them"""

    width = 400; height = 350

    right_eye = resize(right_eye, (width, height))
    left_eye = resize(left_eye, (width, height))
    frame = resize(frame, (width, height))

    displaying = hstack((right_eye, frame))
    displaying = hstack((displaying, left_eye))

    return displaying



def displaying(frame, analyse, watch, right_eye, left_eye):
    """We make the top part who's analyse and bottom who's video for the display"""

    displaying_analyse = part_analyse(analyse, watch)
    displaying_video = part_video(frame, right_eye, left_eye)
    horizontal_concat = vstack( (displaying_analyse, displaying_video) )

    return horizontal_concat



def eyes_display(frame, gray, landmarks, eyes_movements, eye_display, counter_frame):
    """Here's the main function"""

    
    raising = False
    #Recuperate movement of eyes
    if eyes_movements != None:
        for i in eyes_movements:
            eye_display.append(i)

    #We del the list in case no movements
    if eye_display != [] and eyes_movements == None:
        raising = True

    #Recuperate eyes dlib points
    right_eye_points = convexHull(array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)]))
    left_eye_points = convexHull(array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)]))

    #Treating our crops
    right_crop, _, _, _, _, _,_  = work_on_eye_picture(right_eye_points, frame)
    left_crop, border_height, border_width, x, y, w, h = work_on_eye_picture(left_eye_points, frame)

    #Making arrows
    right_eye, _ = animations(border_height, border_width, x, y, w, h, right_crop, eye_display)
    left_eye, watch = animations(border_height, border_width, x, y, w, h, left_crop, eye_display)

    #Display the top and bot parts with analyse
    analyse = [",npo,p", "j)l$^m$", "jçh_gè"]
    horizontal_concat = displaying(frame, analyse, watch, right_eye, left_eye)

    imshow("eyes", horizontal_concat)

    return raising
    
