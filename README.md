# .covi files convertor
Simple script to extract measured data from multiple .covi files and save them to csv/txt files. 

.covi file contains measured force / pressure data from [GTE CoboSafe measuring device](https://www.gte.de/product/force-measuring-systems-for-collaborating-robots/?lang=en, "Force and Pressure Measurement System for Collaborative Robots").

## Output

Force data are saved to csv file - two columns for each measurement  (Time [s], Force [N]).

Pressure data can be saved either to csv file (one column for each measurement) or to txt file (individual file for each measurement).

## Usage
[examples](examples) folder contains a few .covi files.

These .covi files can be converted by calling [covi_convertor_main.py](covi_convertor_main.py) as 
* convert force data (2020_03_11 Force measurement 36.covi)
  > python3 covi_convertor_main.py 0 output_name examples/2020_03_11\ Force-pressure\ measurement_1
* convert pressure data (2020_03_11 Pressure measurement_1.covi)
  > python3 covi_convertor_main.py 1 output_name examples/2020_03_11\ Force-pressure\ measurement_1
* convert both force and pressure data (2020_03_11 Force measurement 36.covi & 2020_03_11 Pressure measurement_1.covi)
  > python3 covi_convertor_main.py 2 output_name examples
  
However, the preffered way is to import [covi_convertor.py](covi_convertor.py) to your own code and call functions **force_to_csv**, **pressure_to_csv**, **force_pressure_to_csv** directly.
