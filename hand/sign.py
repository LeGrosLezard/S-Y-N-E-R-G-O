def sign(pouce, index):
    try:
        if abs(pouce[-1][1][0] - index[-1][1][0]) <= 10 and\
           abs(pouce[-1][1][1] - index[-1][1][1]) <= 10:
            print("index pouce rond")
    except:
        print("ERROR SIGN")
