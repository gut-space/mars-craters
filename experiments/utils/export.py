import math
import csv
import shapefile

def relative_picture_coordinates_to_degrees(craters, center_coordinates, width, height, ppd):
    center_lng, center_lat = center_coordinates
    left_up_lng = center_lng - (width / 2) / ppd
    left_up_lat = center_lat + (height / 2) / ppd

    result = []

    for x, y, r in craters[0,:]:
        crater_lng = left_up_lng + x / ppd
        crater_lat = left_up_lat - y / ppd
        radius = ((2 * math.pi * 3396.2) / 360) * (r / ppd)
        
        result.append((crater_lng, crater_lat, radius))

    return result

def save_csv(craters, output_path="output.csv"):
    with open(output_path, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(("Longitude", "Latitude", "Radius"))
        
        for lng, lat, r in craters:
            spamwriter.writerow((lng, lat, r))

def save_shapefile(craters, output_path="output.shp"):
    with shapefile.Writer(output_path, shapeType=shapefile.POINT) as shp:
        shp.field("RADIUS", fieldType="N", decimal=8)
        for lng, lat, r in craters:
            shp.point(lng,lat)
            shp.record(RADIUS=r)
