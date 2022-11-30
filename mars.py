import cv2
import numpy as np
from os import path, remove
import argparse

from utils import automatic

IMG_EXAMPLE = "./img/P17_007703_2313_XN_51N345W.jpeg"

DATA_DIR = "./experiments/org"

FILES = [ "THEMIS Night IR 100m Global Mosaic (v14.0)_JM137.184_-15.195_256_2048ppd.jpg" ]
       #, "THEMIS Night IR 100m Global Mosaic (v14.0)_JM137.184_-15.195_256_2048ppd_2_with_craters_max_diameter_30_km_min_crater_depth_0.5_km.jpg" ]

CIRCLES = (
    (150, 10, 50),
    (550 , 50, 500)
)

def preprocess_edges_canny(img):

    """ Implements Canny edges detection.

        For details, see: https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html

    """

    print("Running Canny edge detection.")

    threshold_low = float(100) # first threshold for the hysteresis procedure.
    threshold_high = float(200) # second threshold for the hysteresis procedure.
    sobel_aperture_size = 3 # aperture size for the Sobel operator.
    l2gradient = False # a flag, indicating whether a more accurate, but slower gradient should be used

    # now create an array of the same dimension, but only one channel
    e = np.zeros((img.shape[0], img.shape[1]))

    # Call the canny image search
    edges = cv2.Canny(img, threshold_low, threshold_high, e, sobel_aperture_size, l2gradient)

    return edges

def preprocess_edges_sobel(img):
    print("Running sobel edge detection.")

    grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=3)

    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    return grad

def preprocess_median_blur(img, blur_radius):

    # blur_radius - a good values are between 5 and 15
    return cv2.medianBlur(img, blur_radius)



def preprocess_file(f: str, step1_file: str, step2_file: str, args):

    img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)

    # smoothes an image using the median filter with the ksize×ksize aperture, must be odd number
    median_blur = args.blur

    img2 = preprocess_median_blur(img, median_blur)

    cv2.imwrite(step1_file, img2)
    if args.display_steps:
        cv2.imshow('Edges', img2)
        cv2.waitKey(10000)
    print(f"3. Median blur (step 1) stored in {step1_file}")

    if args.edges == 'sobel':
        img3 = preprocess_edges_sobel(img2)
    elif args.edges == 'canny':
        img3 = preprocess_edges_canny(img2)
    elif args.edges == 'none':
        print("Skipping edges detection.")
    else:
        print(f"ERROR: Invalid edge detection algorithm specified: {args.edges}")

    cv2.imwrite(step2_file, img3)

    print(f"4. Edge detection (step 2) stored in {step2_file}")
    if args.display_steps:
        cv2.imshow('Edges', img3)
        cv2.waitKey(10000)

def show_file(f: str):
    # Load a sample image
    img = cv2.imread(f)
    show_img(img)

def show_img(img):
    # Display the image, wait for key and quit
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

### Main section starts here

if __name__ == '__main__':

    parser = argparse.ArgumentParser("gut-space-craters")
    parser.add_argument("--blur", type=int, help='Specifies median blur radius.', default=5)
    parser.add_argument("--edges", type=str, help='Specifies the edge detection algorithm (sobel, canny, none)', default='sobel')
    parser.add_argument('-f','--file', type=str, nargs='+', action='append', help='list of PNG or JPEG files to process.')
    parser.add_argument('-s','--save-steps', type=bool, help='Specifies if intermediate steps should be saved', default=True)
    parser.add_argument('-d','--display-steps', type=bool, help='Specifies if intermediate steps should shown', default=False)
    args = parser.parse_args()

    if args.file is None:
        print(f"No files specified, using detault {FILES}")
        args.file = FILES

    print(f"Running with the following parameters: {args}")

    for f in FILES:
        fname = path.join(DATA_DIR, f)
        print(f"1. Processing file {fname}")

        fname_base, _ = path.splitext(fname)

        meta = automatic.get_meta(fname)
        print(f"2. Metadata: {meta}")

        step1_file = fname_base + "_1_blur.jpg"
        step2_file = fname_base + "_2_edges.jpg"
        step3_file = fname_base + "_3_craters.jpg"
        step4_file = fname_base + "_4_craters.shp"

        # Skip the preprocessing first and assume the input file is preprocessed
        preprocess_file(fname, step1_file, step2_file, args)

        craters = automatic.load_recognize_circles_and_display(CIRCLES, fname, step2_file, step3_file)
        automatic.export_to_csv_and_shp(craters, meta)

        if not args.save_steps:
            for f in [step1_file, step2_file]:
                if path.exists(f):
                    remove(f)
