import cv2
from .circle_recognition import simply_circle_recognition
from .display import show_circles

def load_recognize_circles_and_display(org_path, preprocess_path, circle_parameters, save_path=None):
    img_org = cv2.imread(org_path)
    img_preprocess = cv2.imread(preprocess_path)

    circles = simply_circle_recognition(img_preprocess, circle_parameters)
    out_img = show_circles(img_org, circles)

    if save_path is not None:
        cv2.imwrite(save_path, out_img)