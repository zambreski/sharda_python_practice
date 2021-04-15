# -*- coding: utf-8 -*-
"""

PURPOSE: Retreive selected variables from a kansas mesonet station from start
to end dates.

    Final units:  
            Temperature: deg C
            Solar: mJ m-2 day-1
            Wind: km/day
            RH:%

INPUTS:
        (1) climate variables desired
        (2) station
        (3) start and end dates.  
    
OUTPUTS:
        (1) CSV

AUTHOR: Zachary Zambreski, 2021

REFERENCES:
    
    See http://mesonet.k-state.edu/rest/ for more information!

"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import numpy as np
import pandas as pd
import requests
import datetime

#------#
# MAIN #
#------#

if __name__== "__main__":
 
    #--------#
    # INPUTS #
    #--------#

    # Main directory to store output for Ag-Climate update
    outDir = ('./')
    
    # Location of REST service
    urlBase = 'http://mesonet.k-state.edu/rest/stationdata/'
    
    # Mesonet variables to obtain
    # If you dont' specify, it will return all available 
    # EVAPOTRANS variable (e.g. ET) is not included on the REST server?!?
    # Manually retreived from the web and added as extra column...
    climVars = 'TEMP2MMAX,TEMP2MMIN,PRECIP,WSPD2MAVG,RELHUM2MAVG,SR'
    
    # Final column names
    colNames = {'TIMESTAMP':'Date','TEMP2MMAX':'tasmax','TEMP2MMIN':'tasmin','PRECIP':'pr',
                'WSPD2MAVG':'wind','RELHUM2MAVG':'rh','SR':'rsds',}
    
    stations  = ['Garden City','Lane','Roth Tech Farm']      # 'all' for allstations
    interval  = 'day'              # Day, hour, 5min
    
    # Date information
    start     = datetime.datetime(2020,4,15)
    end       = datetime.datetime(2020,10,15)
  
#%%---------------------------------------------------------------------------#

    for station in stations:
    
        #----------------------#
        # Collect Mesonet data #
        #----------------------#
        
        # shift date by 1 because the dates will be for the 24 previous hours..
        sShift = start + datetime.timedelta(days=1)
        eShift = end + datetime.timedelta(days=1)
        
        startTime = '%s000000'%(sShift.strftime('%Y%m%d')) 
        # End day of month             
        endTime = '%s000000'%(eShift.strftime('%Y%m%d'))  
        
        params =[('stn',station), ('int',interval), ('t_start',startTime),
                ('t_end',endTime),('vars',climVars)]
        
        # Make the request
        response = requests.get(urlBase, params = params)
        data = response.text
        
    #%%---------------------------------------------------------------------------#
        
        #---------------------#
        # Organize into table #
        #---------------------#
            
        returnedLines = [line.split(',') for line in data.split('\n')]
        df =  pd.DataFrame(returnedLines)
        df.columns = df.iloc[0]
        df = df.reindex(df.index.drop(0))
    
        df = df.replace('M', np.nan) # Missing data to nan
        df[climVars.split(',')] =  df[ climVars.split(',')].apply(pd.to_numeric) 
        df['TIMESTAMP'] =  pd.to_datetime(df['TIMESTAMP'], 
                                          format = '%Y-%m-%d %H:%M:%S') 
        
        # Offset by one day
        # Periods are summarized for the previous 24 hours for the daily interval
        df['TIMESTAMP']=  df['TIMESTAMP'] - pd.DateOffset(1)
        
        # Rename columns (axis 1)
        df = df.rename(colNames,axis=1)
        
 #%%---------------------------------------------------------------------------#
        
        #-------------------#
        # Convert and write #
        #-------------------#
        
        # Convert wind speed from m/s to km/day
        df['wind'] = df['wind'] *86.4
        df = df.drop(['STATION'],axis=1)
        
        # Write to file   
        oFile_Name = outDir + '/%s_%s_%s.csv'%(station,start.strftime("%Y%m%d"),
                                                     end.strftime('%Y%m%d'))
        df.to_csv(oFile_Name,index=False,columns = colNames.values())
        