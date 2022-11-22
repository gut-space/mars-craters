import cv2
import os
from .circle_recognition import simply_circle_recognition
from .display import show_circles
from .export import relative_picture_coordinates_to_degrees, save_csv, save_shapefile

def load_recognize_circles_and_display(circle_parameters, org_path, preprocess_path="input.jpg",  save_path="output.jpg"):
    img_org = cv2.imread(org_path)
    img_preprocess = cv2.imread(preprocess_path)

    circles = simply_circle_recognition(img_preprocess, circle_parameters)
    print(circles)
    print(circles.shape)
    out_img = show_circles(img_org, circles)

    if save_path is not None:
        cv2.imwrite(save_path, out_img)

    return circles

def get_meta(path):
    """Gets meta information from the JMARS filename

    :param path: path to the file (can with with or without dirs)
    :type path: string
    :return: structure with width, height, center and ppd (zoom factor)
    :rtype: int, int, (float, float), int
    """
    img = cv2.imread(path)
    height, width = img.shape[:2]

    # First, get rid of the dir
    _, fname = os.path.split(path)

    # Now, get rid of the extension
    fname, _ = os.path.splitext(fname)

    _, lng, lat, _, ppd, *_ = fname.split("_")

    is_jmars = lng.startswith("JM")
    if is_jmars:
        lng = lng.lstrip("JM")

    ppd = int(ppd.rstrip("ppd"))
    lng = float(lng)
    lat = float(lat)

    return {
        "width": width,
        "height": height,
        "center": (lng, lat),
        "ppd": ppd
    }

def export_to_csv_and_shp(craters, img_meta, output_path="output"):
    degree_craters = relative_picture_coordinates_to_degrees(
        craters, img_meta['center'], img_meta['width'], img_meta['height'], img_meta['ppd']
    )
    save_csv(degree_craters, output_path + ".csv")
    save_shapefile(degree_craters, output_path + ".shp")