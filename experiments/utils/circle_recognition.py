import cv2
import numpy as np 

def simply_circle_recognition(img, circle_params):
    img = cv2.cvtColor(img ,cv2.COLOR_BGR2GRAY)
    #Applying Blur to the image
    img = cv2.GaussianBlur(img, (21,21), cv2.BORDER_DEFAULT)

    to_stack_circs = []
    for distance, min_radius, max_radius in circle_params:
        circs = cv2.HoughCircles(img , cv2.HOUGH_GRADIENT,0.9,distance,param1 = 20 , param2 = 30,minRadius=min_radius , maxRadius=max_radius )
        to_stack_circs.append(circs)

    all_circs = to_stack_circs[0]
    for circs in to_stack_circs[1:]:
        all_circs = np.hstack((all_circs, circs))

    all_circs_rounded = np.uint16(np.around(all_circs))
    return all_circs_rounded