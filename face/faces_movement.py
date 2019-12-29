from on_eyes import on_eyes
from mouse import mouse

def face_movements(landmarks, frame, head_box):

    #Recuperate On eye movements
    on_eye_movemement = on_eyes(landmarks, frame, head_box)
    #if on_eye_movemement[0] != "": print(on_eye_movemement[0])
    #if on_eye_movemement[1] != "": print(on_eye_movemement[1])

    smyle, side_smyle = mouse(landmarks, frame, head_box)
    if smyle != "": print(smyle)
    if side_smyle != "": print(side_smyle)
