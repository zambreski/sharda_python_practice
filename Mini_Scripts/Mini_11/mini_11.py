# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: Introduction to application programming interface (API)
    
    Objective: Automate download of USDA NASS data    
    
    Here we show an alternative for retreiving data from USDA NASS database rather than
    the online form selection tool. The advantages of this method besides automation
    of data colleciton include easy post-processing of the data frame after
    retreival. 

    New pythonpackages: request and json
  
    Many databases have automative functunality though the use of APIs.  
    
    README MORE HERE:   
        https://quickstats.nass.usda.gov/api
 
    
INPUTS:
    
    (1) NASS URL
    (2) NASS API KEY
    (3) Payload with data information
    
OUTPUTS:
    
    (1) CSV files

AUTHOR: Zachary Zambreski, Kansas State University (2020)

Created on Thu Dec  24 12:48:14 2020

"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import pandas as pd
import requests, json

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
    
    # Location of the API (doesn't change)
    url = 'http://quickstats.nass.usda.gov/api/api_GET/'
    
    # API key is unique to the user. You sign up for a key
    # Below is my key (Zach Zambreski)
    # Request one here: https://quickstats.nass.usda.gov/api 
    api_key =  "41FEE8FF-56AD-32E4-96CE-E4E746E30181"
    
    # Here is where we specify the type of data from NASS we want! 
    # It is a python dictionary.
    # payload = {'key':api_key,'param':{parameter}} i.e. 'source_desc'
    # Info on how to use/sructure this call to the API:
    # https://quickstats.nass.usda.gov/api
    # Many different options
    # ** If you don't specify correectly, the call will return with an error
    # Dont request too much data. Max is 50,000 per call
    
    payload = {'source_desc':'SURVEY',
        	   'commodity_desc':'CORN',
               'util_practice_desc':'GRAIN',
        	   'statisticcat_desc':'YIELD',
        	   'agg_level_desc':'COUNTY',
        	   'format':'JSON',
        	   'unit_desc':'BU / ACRE',
        	   'prodn_practice_desc':'ALL PRODUCTION PRACTICES',
               'state_alpha': 'KS'}
    
    # Start and end years to collect data. If you request outside of available
    # data range, it will just return all available data
    # Remember the more years you select, the more data!
    startYear = 1950
    endYear   = 2019

    # States to access
    states = ['KS']

    # Location to store output
    outLoc = ('.')

#%%---------------------------------------------------------------------------#
 
    # year range, remember python indexing
    years = list(map(str,range(startYear,endYear+1)))

    # Add this key and value pair into the dictionary
    payload['year'] = years
    payload['key']  = api_key

    # Returns a response object
    # Use the base url and pass the payload
    # It may take some number of seconds to receive the quest
    r = requests.get(url,params=payload)
    
    print('Here is what you actually sent to the API (it is a url)')
    print('Copy and paste below url into your web browser.It will work!\n')
    print(r.url)

    # get the json data into a pandas dataframe
    # json: Javascript Notation 
    # Lots of APIS use this data structure (web-based)
    df = pd.read_json(json.dumps(r.json()),orient='split')
    
    print(df)
    print(df.columns)

#%%--------------------------------------------------------------------------#
    
    #-------------------------------------------------------------#
    # Examples how you may want to process and save the dataframe #
    #-------------------------------------------------------------#
    
    #
    # Save the dataframe to csv file "as is"
    #
    outFile = '%s/%s_%s.csv'%(outLoc,payload['state_alpha'],
                              payload['commodity_desc'])   
    df.to_csv(outFile)
    
    #
    # Sort the dataframe by 'year' column the save
    #
    df2 = df.sort_values(['year'])
    outFile = '%s/%s_%s_sort.csv'%(outLoc,payload['state_alpha'],
                                   payload['commodity_desc'])
    df2.to_csv(outFile)
    
    #
    # Subset dataframe to only a single county and save
    #
    county = 'RILEY'
    df3 = df2[df2['county_name']=='%s'%(county)]
    outFile = '%s/%s_%s_sort_%s.csv'%(outLoc,payload['state_alpha'],
                                      payload['commodity_desc'],county)
    df3.to_csv(outFile)
