import cv2
import numpy as np
from os import path, remove
import argparse
import sys

sys.path.append('./experiments')

from utils import automatic

DATA_DIR = "./experiments/org/"

FILES = [ DATA_DIR + "THEMIS Night IR 100m Global Mosaic (v14.0)_JM137.184_-15.195_256_2048ppd.jpg",
          DATA_DIR + "THEMIS Night IR 100m Global Mosaic (v14.0)_JM137.184_-15.195_256_2048ppd_2_with_craters_max_diameter_30_km_min_crater_depth_0.5_km.jpg" ]

CIRCLES = (
    (150, 10, 50),
    (550 , 50, 500)
)

def preprocess_edges_canny(img, threshold_low = 100.0, threshold_high = 200.0, sobel_aperture_size = 3):

    """ Implements Canny edges detection.

        For details, see: https://docs.opencv.org/3.4/da/d22/tutorial_py_canny.html

    """

    print("Running Canny edge detection.")

    l2gradient = False # a flag, indicating whether a more accurate, but slower gradient should be used

    # now create an array of the same dimension, but only one channel
    e = np.zeros((img.shape[0], img.shape[1]))

    # Call the canny image search
    edges = cv2.Canny(img, threshold_low, threshold_high, e, sobel_aperture_size, l2gradient)

    return edges

def preprocess_edges_sobel(img, ksize=3):
    print("Running Sobel edge detection.")

    grad_x = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=ksize)
    grad_y = cv2.Sobel(img, cv2.CV_64F, 0, 1, ksize=ksize)

    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)

    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    return grad

def preprocess_median_blur(img, blur_radius):

    print(f"Running median blus with blur radius {blur_radius}.")

    # blur_radius - a good values are between 5 and 15
    return cv2.medianBlur(img, blur_radius)

def preprocess_file(f: str, step1_file: str, step2_file: str, args):

    img = cv2.imread(f, cv2.IMREAD_GRAYSCALE)

    # smoothes an image using the median filter with the ksize×ksize aperture, must be odd number
    median_blur = args.blur
    threshold_low = args.canny_threshold_low # first threshold for the hysteresis procedure.
    threshold_high = args.canny_threshold_high # second threshold for the hysteresis procedure.
    canny_aperture_size = args.canny_aperture_size # aperture size for the Sobel operator.
    sobel_ksize = args.sobel_kernel_size

    img2 = preprocess_median_blur(img, median_blur)

    cv2.imwrite(step1_file, img2)
    if args.display_steps:
        cv2.imshow('Edges', img2)
        cv2.waitKey(10000)
    print(f"3. Median blur (step 1) stored in {step1_file}")

    if args.edges == 'sobel':
        img3 = preprocess_edges_sobel(img2, sobel_ksize)
    elif args.edges == 'canny':
        img3 = preprocess_edges_canny(img2, threshold_low=threshold_low, threshold_high=threshold_high, sobel_aperture_size=canny_aperture_size)
    elif args.edges == 'none':
        print("Skipping edges detection.")
        img3 = img2
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
    parser.add_argument("--blur", type=int, help='Specifies median blur radius.', default=13)
    parser.add_argument("--edges", type=str, help='Specifies the edge detection algorithm (sobel, canny, none)', default='canny')
    parser.add_argument('-f','--file', type=str, nargs='+', action='append', help='list of PNG or JPEG files to process.')
    parser.add_argument('-s','--save-steps', type=bool, help='Specifies if intermediate steps should be saved', default=True)
    parser.add_argument('-d','--display-steps', type=bool, help='Specifies if intermediate steps should shown', default=False)
    parser.add_argument('--geometry', type=str, help='Specifies image geometry (longitude,lattitude,pixels-per-degree), will be determined automatically from the filename if THEMIS naming convention is followed')

    # Canny edge detection parameters:
    parser.add_argument('--canny-threshold-low', type=float, help="Canny: First threshold for hysteresis procedure, default=100.0", default=100.0)
    parser.add_argument('--canny-threshold-high', type=float, help="Canny: Second threshold for hysteresis procedure, default=200.0", default=200.0)
    parser.add_argument('--canny-aperture-size', type=int, help="Canny: aperture size for the Sobel operator, default=3", default=3)

    # Canny edge detection parameters:
    parser.add_argument('--sobel-kernel-size', type=int, help="Sobel: size of the kernel, default=3", default=3)

    args = parser.parse_args()

    if args.file is None:
        print(f"No files specified, using default {FILES}")
        args.file = FILES
    else:
        # argparse has an odd notation. It returns list of lists of strings if
        # repeated arguments are allowed (as is the case for -f). Need to get
        # rid of inner lists.
        args.file = list(map(lambda a: a[0], args.file))

    print(f"Running with the following parameters: {args}")

    for f in args.file:
        #fname = path.join(DATA_DIR, f)
        fname = f
        print(f"1. Processing file {fname}")

        fname_base, _ = path.splitext(fname)

        meta = automatic.get_meta(fname, args.geometry)
        print(f"2. Metadata: {meta}")

        step1_file = fname_base + "_1_blur.jpg"
        step2_file = fname_base + "_2_edges.jpg"
        step3_file = fname_base + "_3_craters.jpg"
        step4_file = fname_base + "_4_craters"

        # Skip the preprocessing first and assume the input file is preprocessed
        preprocess_file(fname, step1_file, step2_file, args)

        craters = automatic.load_recognize_circles_and_display(CIRCLES, fname, step2_file, step3_file)
        automatic.export_to_csv_and_shp(craters, meta, output_path = step4_file)

        if not args.save_steps:
            for f in [step1_file, step2_file]:
                if path.exists(f):
                    remove(f)
