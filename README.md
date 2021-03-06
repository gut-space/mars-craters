# Mars Craters Project
## How to get data

You can fetch the Mars data from different sources. NASA provides some WMTS and WMS services.
You can explore them using QGIS. But it has a one problem - QGIS has poorly support for Mars coordinate systems and it is comfortable.

Better choice is JMARS app. It allow you to explore data from many missions and sensors, easy search and visualize data. You can also export them to high resolution images and vector data.

## Main idea

During our research we noticed that some impact craters has very bright edges on imageries from infrared sensor at night from THEMIS mission. NASA provide the global mosaic from these images in resolution 100m. It is good for recognize craters.

Using this data has one limitation: not each crater has bright edge. Crater must to have a specific depth (at least 0.4-0.5 km). The radius cannot be too big (< 15km).

We noticed that not only craters have bright edge on images. Other terrain form may to have similar behavior. It is a problematic and we need to filter it.

In filtration stage we based on shape. We assume that impact crater have rounded shape. We use a circle recognition algorithm (for example Hough Circle Transform with Hough Gradient detection method).

During filtration you should remember that not whole edge will be bright for each crater. For old crater edge may be incomplete or edge may to have different structure and some parts are dark.

## Selected area

Presented method search for specific subset of craters. You should select flat terrain without mountains, because when terrain is higher than it warm up more and has stronger bright in infrared.  
Area shouldn't contains too big craters. Algorithm cannot recognize it.  And craters shouldn't be too thick. We assume that exists space between two craters.  
Probably you should to select area near equator. The farther than equator meteorite hit at greater angle and impact crater may be more ellipsoidal (it decrease accuracy of circle detect algorithm).  

## Tools

For explore the data we used JMARS. Next JMARS image was preprocess using GIMP. Then we use Python and OpenCV to perform circle detection and export output image and shapefile with result. At the end we use QGIS to compare recognized craters with real (crater database is provided by JMARS).

## Algorithm

Input image has resolution 2048 pixels per degree.

1. Convert image to one band Grayscale  
   THEMIS mosaic is already in  grayscale but JMARS export it to JPEG which has RGB data.
2. Blur the image using Median Blur  
   We need to blur image to remove noises (from JPEG compression) and small geometric noises (small bright areas). We noticed that median blur is better then Gaussian for it, because it stronger blur small objects than bigger (for example craters).  
   We used parameters:

   * Neighborhood: Circle
   * Radius: 12
   * Percentile: 66
   * High precision enabled

   Too small radius don't remove geometric noises, too big remove small craters.  
   You need adjust the radius for you resolution. Percentile should be universal.  
   Neighborhood "circle" has minimal better result than other.

3. Detect edges using Edge GIMP method  
   This step should to remove background pixels and keep only crater and hills. The best if this step assign higher value for crater edge pixels and lower for other edges.  
   We used parameters:

   * Algorithm: Gradient
   * Amount: 1

   We test all available algorithm. Gradient and Laplace are useful for us. As you can read in documentation "Gradient" return "Edge thinner, less contrasted and more blurred than Sobel". But we notice that it the width of detected line is higher for crater edges then other edges.  
   Amount value is minimal. It return high-contrasted image with thin edges.

4. Detect edges using Sobel method
   We repeat edge detection. This step should increase detected crater edges which have a regular shape and decrease other edge which are randomly. Therefore we use simply algorithm which search for straight lines. Due detect circles we need to apply it in horizontal and vertical plane in the same time.

5. Detect circles
   We use a Hough Circle Transform with Hough Gradient detection. We set:
   
   * inverse ratio resolution: 0.9
   * upper threshold for the internal Canny edge detector (param1): 20
   * threshold for center detection (param2): 30

   Next we detect circles twice on the same image. First we search for circles with radius in range from 10 to 50 (pixels, depends on PPD) and distance between centers 150 pixels.
   Next we search for circles with radius in range from 50 to 500 pixels and distance between centers 550 pixels.

   It allow use to detect wide range of radius craters without overlaps.

As result of these steps you get a list of center and radius craters in pixels. Next you need to transform it to meters using PPD and coordinates of image.

## Results

We choose the image from THEMIS Night IR 100m Global Mosaic (v14.0) layer.   
Center has coordinates: 137.184E, -15.195.  
Height: 185 km, width: 312 km.  
Resolution: 2048 pixels per degree.

We assume that our range of craters to detect was craters with radius less than 15 km and depth greater than 0.5 km.

| Radius  | Count (total/selected) | Detected (total/selected) | Acc. (total/selected) |
| ------- | :--------------------: | :-----------------------: | :-------------------: |
| All     |        347 / 13        |                   64 / 11 |      0.18 / 0.85      |
| >= 5 km |         20 / 4         |                     4 / 4 |        0.2 / 1        |
| < 5 km  |        327 / 9         |                    60 / 7 |      0.18 / 0.78      |

In our range we achieve good accuracy **85%**. We don't have falsy recognition (each our recognition was a crater). 15% recognized craters were outside assumed range.

Crear, big craters were to recognized very good.

## Wrong ways

During our test we notice that some ideas for preprocess image are wrong.

You should avoid using "Dilate" algorithm. It increase visual quality of image, but it decrease the accuracy of detection.

You should avoid preliminary stretch the image. It improve the contrast which allow you easily remove small geometric noises, but remove medium and big non-craters edges (or wide brigh area) is almost impossible

"Threshold" tool isn't so useful as we initially think.

Available DTM mosaic has too low resolution

## What next

1. We need a method for rate edge of our crater, what much is bright
2. We should compare our result with Machine Learning automatic crater detection results (see Wronkiewicz et al.)
3. We have a problem with detect craters with dark center
4. We should preprocess our image multiple times for specific requirements different craters and next detect them from bigger to smaller.

## Bibliography

1. https://opencv-python-tutroals.readthedocs.io/en/latest/ - OpenCV + Python tutorials
2. Hill, J., C. S. Edwards and P. R. Christensen (2014), Mapping the Martian Surface with THEMIS Infrared Global Mosaics, 8th International Conference on Mars, Pasadena, CA, Abs. 1141.
3. Edwards, C. S., K. J. Nowicki, P. R. Christensen, J. Hill, N. Gorelick, and K. Murray (2011), Mosaicking of global planetary image datasets: 1. Techniques and data processing for Thermal Emission Imaging System (THEMIS) multi-spectral data, J. Geophys. Res., 116, E10008, doi:10.1029/2010JE003755.
4. Wronkiewicz, M., Kerner, H.R., Harrison, T. (2018). Autonomous Mapping of Surface Features on Mars. American Geophysical Union (AGU) Fall Meeting, Washington, DC.