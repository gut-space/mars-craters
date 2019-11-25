import cv2
import numpy as np 
import matplotlib.pyplot as plt 

def show_circles(img_org, circles):
    overlay = img_org.copy()
    count =1
    for i in circles[0,:]:
        cv2.circle(overlay,(i[0],i[1]),i[2],(255,0,0),-15)
        cv2.circle(overlay,(i[0],i[1]),2,(255,0,255),23)
        #cv2.putText(img_org, ""+ str(count),(i[0]-70,i[1]+30),cv2.FONT_HERSHEY_SIMPLEX,1.1,(255,0,0),2)
        count +=1

    alpha = 0.2
    img_org = cv2.addWeighted(overlay, alpha, img_org, 1 - alpha, 0)

    plt.rcParams["figure.figsize"] = (16,9)
    plt.imshow(img_org)
    plt.show()
    return img_org