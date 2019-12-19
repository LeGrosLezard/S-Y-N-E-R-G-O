import cv2

video_name = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\a.mp4"
video = cv2.VideoCapture(video_name)
subtractor = cv2.createBackgroundSubtractorMOG2(history=1, varThreshold=5, detectShadows=True)

while True:


    frame = cv2.resize(video.read()[1], (800, 500))
    sub = subtractor.apply(frame)
    a = cv2.countNonZero(sub)

    
    if a > 0 and a >= ((800*500) * 0.625):
        print("CHANGEMENT DE FRAME")



    cv2.imshow('frame', frame)
    cv2.imshow('sub', sub)


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.video.release()
cv2.destroyAllWindows()
