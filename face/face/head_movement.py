"""Let you watch that https://www.youtube.com/watch?v=ibuEFfpVWlU&t=518s"""



from head_points import eyes_points_for_head_analysis

from turn_head import turn_head
from advanced_recedes_head import advanced_recedes_head
from leanning_head import leanning_head
from bent_up_head import bent_up_head
from head_emotion import head_emotion


def head_movement(landmarks, head_box, emotion_classifier, gray):

    #Recuperate right_eye, left_eye, nose
    right_eye, left_eye, nose = eyes_points_for_head_analysis(landmarks)

    #Person moves his head to right or left
    turn = turn_head(right_eye, left_eye, nose, head_box)
    #if turn != "": print(turn)

    #Person leaning his head to right or left
    leanning = leanning_head(right_eye, left_eye, nose, head_box)
    #if leanning != "":print(leanning)

    #Person moves his head to bot or top
    bot_top = bent_up_head(right_eye, left_eye, nose)
    #if bot_top != "": print(bot_top)

    emotion = head_emotion(head_box, emotion_classifier, gray)
    #print(emotion)









