"""Let you watch that https://www.youtube.com/watch?v=ibuEFfpVWlU&t=518s"""


from turn_head import look_right_left
from head_points import eyes_points_for_head_analysis


def head_movement(landmarks, head_box):

    #Recuperate
    right_eye, left_eye, nose = eyes_points_for_head_analysis(landmarks)

    turn = look_right_left(right_eye, left_eye, nose, head_box)
    #if turn != "": print(turn)


















