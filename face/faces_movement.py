from on_eyes import on_eyes
from mouse import mouse
from face_area import face_area
def face_movements(landmarks, frame, head_box):

    if landmarks is not None:

        #Recuperate On eye movements
        on_eye_movemement = on_eyes(landmarks, frame, head_box)
        #if on_eye_movemement[0] != "": print(on_eye_movemement[0])
        #if on_eye_movemement[1] != "": print(on_eye_movemement[1])

        smyle, side_smyle = mouse(landmarks, frame, head_box)
        #if smyle != "": print(smyle)
        #if side_smyle != "": print(side_smyle)

    
        face_area(frame, landmarks)


    else:
        face_area(frame, landmarks)
