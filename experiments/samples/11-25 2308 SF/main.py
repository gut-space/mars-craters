from utils import automatic

ORG_PATH = "../../org/THEMIS Night IR 100m Global Mosaic (v14.0)_JM137.184_-15.195_256_2048ppd_2_with_craters_max_diameter_30_km_min_crater_depth_0.5_km.jpg"

CIRCLES = (
    (150, 10, 50),
    (550 , 50, 500)
)

meta = automatic.get_meta(ORG_PATH)
print(meta)

craters = automatic.load_recognize_circles_and_display(CIRCLES, ORG_PATH)
automatic.export_to_csv_and_shp(craters, meta)
