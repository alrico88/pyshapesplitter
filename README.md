# pyshapesplitter

Python CLI app to split Shapefiles into GeoJSON files by any property, with optional filtering.

## Usage

Clone this repository, navigate to the folder and install dependencies using `pipenv install`.

Then activate the env using `pipenv shell`.

Finally run the CLI app `python3 pyshapesplitter.py` and follow the prompts.

![Demo](https://i.imgur.com/uSzz4Rt.png)

Tested on MacOS 12.4 and Python 3.9.

## Options

The CLI will prompt you about:

- The path to the shapefile (.shp file)
- The property to split the shapefile by (by reading the available columns)
- The column and value(s) to filter by (OPTIONAL)
- The output dir

## Results

Each unique value of the chosen column will result in a GeoJSON FeatureCollection in the specified folder.
