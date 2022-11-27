import cv2
import numpy as np
from os import path
import shutil

from utils import automatic

IMG_EXAMPLE = "./img/P17_007703_2313_XN_51N345W.jpeg"

DATA_DIR = "./experiments/org"

FILES = [ "THEMIS Night IR 100m Global Mosaic (v14.0)_JM137.184_-15.195_256_2048ppd.jpg" ,
          "THEMIS Night IR 100m Global Mosaic (v14.0)_JM137.184_-15.195_256_2048ppd_2_with_craters_max_diameter_30_km_min_crater_depth_0.5_km.jpg" ]

CIRCLES = (
    (150, 10, 50),
    (550 , 50, 500)
)

def edges_canny(img):

    """ Implements Canny edges detection.

        For details, see: https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html

    """

    threshold_low = float(100) # first threshold for the hysteresis procedure.
    threshold_high = float(200) # second threshold for the hysteresis procedure.
    sobel_aperture_size = 3 # aperture size for the Sobel operator.
    l2gradient = False # a flag, indicating whether a more accurate, but slower gradient should be used

    # now create an array of the same dimension, but only one channel
    e = np.zeros((img.shape[0], img.shape[1]))

    # Call the canny image search
    edges = cv2.Canny(img, threshold_low, threshold_high, e, sobel_aperture_size, l2gradient)

    return edges

def preprocess_file(f: str, fout: str):

    # Pretending any preprocessing was done. In fact, just copy over the file.
    print(f"WARNING: Preprocessing is only simulated. Copied file to {f} => {fout}")


    img = cv2.imread(f)

    edges = edges_canny(img)

    cv2.imshow('Edges',edges)

    cv2.waitKey(10000)

    shutil.copyfile(f, fout)

def show_file(f: str):
    # Load a sample image
    img = cv2.imread(f)

    # Display the image, wait for key and quit
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

for f in FILES:
    fname = path.join(DATA_DIR, f)
    print(f"1. Processing file {fname}")

    fname_base, _ = path.splitext(fname)

    meta = automatic.get_meta(fname)
    print(f"2. Metadata: {meta}")

    input_file = fname_base + "_input.jpg"
    output_file = fname_base + "_out.jpg"

    print(f"3. input_file={input_file}, output_file={output_file}")

    # Skip the preprocessing first and assume the input file is preprocessed
    preprocess_file(fname, input_file)

    #craters = automatic.load_recognize_circles_and_display(CIRCLES, fname, input_file, output_file)
    #automatic.export_to_csv_and_shp(craters, meta)

    #show_file(input_file)
