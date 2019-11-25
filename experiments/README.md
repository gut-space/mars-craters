# How start

1. Create virtual environment:
```sh
python -m venv env
```
2. Start virtual environment:
Linux:
```sh
source env/bin/activate
```
Windows:
```sh
env/Scripts/activate
```
3. Install dependencies
```
python setup.py install
```

# Repo format

## Orignal images directory

Directory "org" contains original images. Name should be in format: ```[LAYER_NAME]_[LONGITUDE]_[LATITUDE]_[ZOOM_LEVEL]_[COMMENT].[EXTENSION]``` where "LAYER_NAME" is layer name (or unique part if original name is long) from JMARS.

"Longitude" and "Latitude" are coordinate of center of image in ellipsoid coordinate system in notation DDD.DDD\[N/S/W/E\].  
JMars using confusing method for display coordinates. Latitude 0 is on equator. Above we have positive number and below negative. Longitude has range from 0 to 360 degrees, where on right side of main meridians we count degrees up from 0 and on left side we count degrees down from 360. If you use this method to save coordinates add **JM** prefix before it for example: ```JM67.332_-12.345```. In this coordinate system we don't use parts of world chars (N/S/W/E).

If you use image from other source or you combine multiple layers then you should add text file with the same name as image with description of image content.

"ZOOM_LEVEL" is approximate zoom level used to export.

"COMMENT" section is optional. You may put here additional information about image. For example quality of export.

## Tools directory

Directory "utils" contains useful scripts to use in your algorithm source files.

## Samples directories

Each directory in "samples" is single iteration of Mars craters recognition algorithm.

Directory name: ```[MONTH]-[DAY] [HOUR]:[MINUTE] [ACRONYM]``` where "MONTH", "DAY", "HOUR", "MINUTE" contains date of start work under specific sample. Acronym is acronym of author.

Directory contains:

* **input.jpg** - input image after preprocess
* **README.md** - file with description (format below)
* **output.jpg** - output image after processing
* **main.py** - source code of algorithm

## README format

Your readme MUST contains:

* [ ] Original image filename
* [ ] Preprocessing steps (for example from GIMP) WITH parametr values
* [ ] The most important constants from source code with description
* [ ] Notes about result

