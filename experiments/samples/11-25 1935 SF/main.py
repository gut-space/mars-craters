from utils import automatic

ORG_PATH = "../../org/THEMIS Night IR 100m Global Mosaic (v14.0)_JM137.184_-15.195_256_2048ppd.jpg"
PREPROCESS_PATH = "input.jpg"
OUTPUT_PATH = "output.jpg"

CIRCLES = (
    (150, 10, 50),
    (550 , 50, 500)
)

automatic.load_recognize_circles_and_display(ORG_PATH, PREPROCESS_PATH, CIRCLES, OUTPUT_PATH)
