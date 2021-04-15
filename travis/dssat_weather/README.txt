----------
Raw mesonet data

In the input_mesonet directory, there is the script "get_data.py" that collects weather variables from Kansas Mesonet Rest service for selected stations and dates.
These files are written to separate csv files, which will be used for converting into the .WTH format that can be read by DSSAT.
 
The REST API from the Mesonet does NOT return evapotranspiration, so columns for et were manually added into each csv file. evapotranspiration was retreieved
directly from the web interface at https://mesonet.k-state.edu/.

----------
DSSAT formatted weather data (XXX.WTH)

"wimporter.py" : developed by the CO OWCAP group members and modified by Zach for Travis.

To write the XXX.WTH files, you must alter the configuration file for your station (config_1_weather_importer.xlsx). "wimporter.py" will use this file extract 
weather data for a single station. Make sure the input/output directories, latitude, longitude, station abbreviation, and elevation are correct. 
"wimporter.py" can only handle a single station at a time. Please look over the descriptions in the configuration file carefully.

Run wimporter.py from the command-line or console and it should write the files to the user-selected output directory. 