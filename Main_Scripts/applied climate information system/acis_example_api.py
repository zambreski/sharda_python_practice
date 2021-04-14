# -*- coding: utf-8 -*-
"""

PURPOSE: Simple example of a ACIS web-service call for Kansas stations. ACIS web calls
are more complicated than NASS as there are many more options and operations
that can be performed on the backend server.
    
INPUTS:
    
    (1) Paylod of parameters
    
OUTPUTS:
    
    (1) Pandas table


Reference: http://www.rcc-acis.org/docs_webservices.html


AUTHOR: Zachary Zambreski,  (2021)

Created on Sat Mar  6 10:21:00 2021

"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#
import json
import pandas as pd
import urllib.request

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
    
    # Link specific to the API for getting multiple stations in a single call
    # you need other urls for single station or gridded data.
    url = 'http://data.rcc-acis.org/MultiStnData'
    
    # Parameters to pass to web service . Notice it is a dictionary with embedded
    # lists for more complicated calls
    payload = {"state":"KS",
                  "sdate":"2021-02-01",
                  "edate":"2021-02-28",
                  # return name, sid, and lat/lon station
                  "meta":"name,sids,ll", 
                  # Retreive precip for stated period, reduce daily by
                  # summing the data for the month
                  "elems":[{"name":"pcpn","interval":"mly","duration":"mly",
                                               "reduce":{"reduce":"sum",
                                                         "add":"mcnt"},
                                               # If more than 3 dates are missing, 
                                               # make invalid
                                               "maxmissing":3,
                                              }]}

#%%--------------------------------------------------------------------------#

    #---------------#
    # Make the call #
    #---------------#

    params2 = urllib.parse.urlencode({'params':json.dumps(payload)}).encode("utf-8")
    req     = urllib.request.Request(url,params2, {'Accept':'application/json'})
    
    response = urllib.request.urlopen(req)
    decode   = json.loads(response.read())
    
    # Extract the data from the call
    data = decode['data']

#%%--------------------------------------------------------------------------#
    #-----------------------#
    # Process returned data #
    #-----------------------#
    
    # Number of stations
    nStations = len(data)
    print('Number of stations retrieved: {}'.format(nStations))
    
    # Show the first station. You can see how this dictionary is structured.
    # It contains 3 keys: 'meta', 'data',
    print(data[0])
    
    # Print the proper name of the first 10 stations
    for s in range(10):
        print(data[s]['meta']['name'])
    
    #
    # Put the data into a nice table
    #
    
    # Create a blank dataframe with 2 columns
    outDF = pd.DataFrame(columns= ['Name','Precip'])
    
    # Iterate all stations
    for s in range(nStations):
        name = data[s]['meta']['name']
        cvar = data[s]['data'][0][0][0]
        outDF.loc[s,'Name']   = name
        outDF.loc[s,'Precip'] = cvar
    
    # Process trace and missing values
    outDF['Precip'][outDF['Precip'] == 'T'] =  0 # Trace to 0
    
    # Convert missing to nan/ convert column to numeric
    outDF['Precip'] = pd.to_numeric(outDF['Precip'], errors='coerce')
    
    # Assign the row index as the station name
    outDF = outDF.set_index('Name')
    
    # Print some quick statistics
    print(outDF.describe())
    
    # Save the table
    outDF.to_excel('./acis_data.xlsx')
