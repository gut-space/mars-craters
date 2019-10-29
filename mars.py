import cv2
import opencv_wrapper as cvw

IMG_DIR = "./img"

# Load a sample image
img = cv2.imread(IMG_DIR + "/" + "P17_007703_2313_XN_51N345W.jpeg")

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
