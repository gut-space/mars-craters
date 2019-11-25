# 11-25 19:35 SF

Original filename: THEMIS Night IR 100m Global Mosaic (v14.0)_JM137.184_-15.195_256_2048ppd.jpg

## Algorithm

0. Mode: Grayscale
1. Median blur (Radius: 12, Percentile: 66)
2. Edge (Algorithm: Gradient, Amount: 1)
3. Sobel

## Notes

- Operation "Dilate" provide a lot of errors
- Combine multiple edge-detection methods allows remove the non-craters edges (non rounded)
- Median blur is better blur for edge detection than others
- Preliminary histogram stretching isn't good. It enhances detection of high quality craters, but decrease low and increase noises
- This method don't detect very small craters
- This algorithm has a problems with detect medium craters with dark center