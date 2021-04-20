# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: Introduction to Google Earth Engine (GEE)
    
    Objective: Create a figure with two axes that show summer average NDVI for Eastern
    Kansas River Basin in 2012 vs. 2019.
    Backend will be performed on Google Earth Engine servers
    
    Google Earth Engine has amazing functionality for processing earth-based 
    datasets, and the best part is that the brunt of the work is done on their
    side, not your machine. 
    
    Benefits: 
        We don't need to have these datasets on our machine. If you have
    not worked with satellite datasets, they are QUITE large. 
    
    Drawbacks:
        You are limited to how much you can use GEE for free. The more data crunching,
        the more resources required on the backend. Be mindful of this.
    
    New python packages: earthengine-api
  
    Many databases have automative functunality though the use of APIs.  
    
    README MORE About download:
        https://developers.google.com/earth-engine/guides/python_install-conda
        
        https://developers.google.com/earth-engine/guides/python_install

 
    
INPUTS:
    
    (1) EE URL
    (2) EE API KEY (your credentials)
    (3) Payload with data information
    
OUTPUTS:
    
    (1) CSV files

AUTHOR: Zachary Zambreski, Kansas State University (2020)

Created on Thu Dec  24 12:48:14 2020

"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import ee
import datetime

#------------------------#
# USER-DEFINED FUNCTIONS #
#------------------------#

#------#
# MAIN #
#------#

if __name__== "__main__":
    
    #--------#
    # INPUTS #
    #--------#
    
    
    # Initialize the Earth Engine module.
    # It will tell you that you need to authenticate if it's your first time
    # Just follow the instructions on your screen. Type the command in your 
    # anaconda prompt terminal window
    
    # Once you do this, you will have access to all the back-end functionality
    ee.Initialize()
    
    # Print metadata for a DEM dataset.
    print(ee.Image('USGS/SRTMGL1_003').getInfo())
    
    # Convert ee.Date to client-side date
    ee_date = ee.Date('2020-01-01')
    # Convert back to Python date time object
    py_date = datetime.datetime.utcfromtimestamp(ee_date.getInfo()['value']/1000.0)
    
    # Load a Landsat image.
    img = ee.Image('LANDSAT/LT05/C01/T1_SR/LT05_034033_20000913')
    
    # Print image object WITHOUT call to getInfo(); prints serialized request instructions.
    print(img)
    
    # Print image object WITH call to getInfo(); prints image metadata.
    print(img.getInfo())
    
 #%%-------------------------------------------------------------------------#
 
    # Extract data for a point from the CHRIPS dataset
    #
    # CHIRPS is a daily global precipitation data
    
    # Cambodia
    lat =  12.21
    lon = 105.32 
    
    pointName = "Camboda_%f_%f"%(lat,lon)
    
    # Create a point object in the ee.Geometry class
    p1 = ee.Geometry.Point([lon, lat]);
    
    # Dates
    start = ee.Date('1981-01-01');
    end   = ee.Date('1981-12-31');
    dataset = ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY').filterDate(start,end);
    
    precipitation = dataset.select('precipitation');
    pts = ee.FeatureCollection(ee.List([ee.Feature(p1)]))

    def fill(img, ini):
        """
        
        Function that extracts daily precipitation values for the selected
        point and fills it into a list along with the date.

        Parameters
        ----------
        img : TYPE
            DESCRIPTION.
        ini : TYPE
            DESCRIPTION.

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
       
        newf = ee.FeatureCollection(ini)
      
        # Gets the date of the img
        date = img.date().format("MM/dd/YYYY")
    
        # Gets the values for the points in the current img
        value = img.reduceRegions(pts,ee.Reducer.first())
        
        #print(help(value.map))
        
        def func(f):
            return f.set("date",date)
        
        # Writes the date in each feature
        ft3 = value.map(func)
    
        # merges the FeatureCollections and returns
        return newf.merge(ft3)
    
    # Create an empty Feature Collection object to fill
    ft = ee.FeatureCollection(ee.List([]))
  
    # Iterates over the ImageCollection and puts it into the FeatureCollection
    # object
    newft = ee.FeatureCollection(precipitation.iterate(fill, ft))
    print(type(newft))
    print(type(precipitation.iterate(fill, ft)))
    
    
    # Export excel table to your google drive. This is YOUR drive. Not Zach's.
    task = ee.batch.Export.table.toDrive(collection=newft, 
                                     description='mock_export',
                                     folder='DSSAT_Cambodia',
                                     selectors = (["date","first"]),
                                     fileNamePrefix= pointName)
    
    # Start the above task, which is export command. This task may take
    # some time. 
    task.start()
    
    # Check the status of the task, it may say "RUNNING" for status. Keep printing
    # until it says completed for the state key. This command returns a python
    # dictionary.
    task.status()



