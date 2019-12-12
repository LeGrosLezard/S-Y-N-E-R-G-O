def add_border(img, crop):

    height, width = img.shape[:2]
    height_crop, width_crop = crop.shape[:2]

    addHeight = int((height - height_crop) / 2)
    addWidth = int((width - width_crop) / 2)
    
    crop = cv2.copyMakeBorder(crop, addHeight, addHeight, 
                 addWidth, addWidth, cv2.BORDER_CONSTANT, value= (0, 0, 0))
    return crop
            #left_hand = add_border(frame, left_hand)
            #right_hand = add_border(frame, right_hand)

            #h,w = left_hand.shape[:2]
            #right_hand = cv2.resize(right_hand, (w, h))

            #frame = cv2.resize(frame, (w, h))
            #displaying = np.hstack((left_hand, frame))
            #displaying = np.hstack((displaying, right_hand))
            #displaying = np.hstack((left_hand, right_hand))
