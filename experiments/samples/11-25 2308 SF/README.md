# Recognized craters

| Radius [km] | Real | Recognized | Correct | Accuracy |
| ----------: | ---: | ---------: | ------: | -------: |
|        > 30 |    3 |          0 |       0 |        0 |
|       25-30 |    0 |          0 |       0 |        0 |
|       20-25 |    1 |          0 |       0 |        0 |
|       15-20 |    1 |          0 |       0 |        0 |
|       10-15 |    9 |          3 |       3 |     0.33 |
|        5-10 |    6 |          1 |       1 |     0.16 |
|         4-5 |    5 |            |       4 |      0.8 |
|         3-4 |   10 |            |       2 |      0.2 |
|         2-3 |   17 |            |       4 |     0.24 |
|         1-2 |   55 |            |      20 |     0.36 |
|         < 1 |  240 |            |      30 |     0.13 |

Total craters in area: 347  
Total recognized craters: 64  
Falsy recognized craters: 0  
Total accuracy: 0.18  

## Subset of craters

Different craters have a different characteristic. To recognize craters we used THEMIS Infrared Night sensor. We noticed that some craters have very bright edge on images.

But only craters which have a specific diameter and depth have this effect. If radius was too long than edge of crater has too low high and too damaged edge. If depth was too low than edge has too low high.

Therefore this method is best for recognize craters with radius lower than 15 km and depth higher than 0.5 km.

| Radius [km] | Real | Recognized | Correct | Accuracy |
| ----------: | ---: | ---------: | ------: | -------: |
|     10 - 15 |    3 |          3 |       3 |        1 |
|      5 - 10 |    1 |          1 |       1 |        1 |
|       4 - 5 |    4 |            |       4 |        1 |
|       3 - 4 |    2 |            |       1 |      0.5 |
|       2 - 3 |    3 |            |       2 |     0.66 |
|         < 2 |    0 |            |         |        - |

Total craters: 13  
Not recognized craters: 2  
Accuracy: 0.85  

# Notes

Algorithm don't recognize the craters with dark center.