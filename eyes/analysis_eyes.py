"""Here analysis"""

blink_history = []

def blink_analysis(result, nb_frame, blinking_frame):

    global blink_history

    if result != "":
        print(result)
        blink_history.append(nb_frame)

    if blinking_frame == 0 and len(blink_history) > 0:
        print("closed : ", len(blink_history),
              "from ", blink_history[0], "to ", blink_history[-1], "frames")
        blink_history = []
