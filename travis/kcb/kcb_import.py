# -*- coding: utf-8 -*-
"""

PURPOSE: Create input forcing data files for basil crop coefficient for DSSAT.
MAke sure it matches the length of the 

    
INPUTS:
    
    (1)
    
OUTPUTS:
    
    (1)

AUTHOR: Zachary Zambreski, Kansas State University (2021)

Created on Mon May  3 08:52:23 2021

"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import pandas as pd
from pathlib import Path

#--------#
# INPUTS #
#--------#

START_DATE = '4/15/2020'
END_DATE   = '10/15/2020'
FILE_CONFIGURATION_1 = 'kcb_import_control.xlsx'


#------#
# MAIN #
#------#

if __name__== "__main__":
    
  
    HEADER_TEXT = (
    '*DAILY CROP COEFFICENTS (KCB) values\n\n'
    '!Values were modeled using geospatial vegetation index imagery at the field scale\n'
    '!Values are directly forced in the PETPEN subroutine in the SPAM module\n'
    '!Modelers: Travis Wiederstein, Vaishali Sharda, Zachary Zambreski\n'
    '!Kansas State University\n'
    '!May 2021\n\n'
    )
    
    try:
        
        df_config = pd.read_excel(FILE_CONFIGURATION_1,
                        sheet_name='config_1', skiprows=2, index_col=0,
                        usecols=[0, 1], header=1)       
        # configuration parameters
        TARGET_FILE = str(df_config.at['target_file', 'Value'])
        OUT_DIRECTORY = Path(str(df_config.at['out_directory', 'Value']))
        STATION_PREFIX = str(df_config.at['station_prefix','Value'])[:2].upper()
        DATE_COL = str(df_config.at['date_col', 'Value'])
        VAL_COL = str(df_config.at['val_col', 'Value'])
    
    except Exception as e:
        print(e, '\nFailed to import configuration!', end='\n')
        input("Enter any key to quit.")
    
    # Open the input file
    try: 
         # import csv
         dfk   = pd.read_csv(TARGET_FILE)
         DATES = pd.DatetimeIndex(pd.to_datetime(dfk[DATE_COL]))
         KCB   = dfk[[DATE_COL,VAL_COL]].set_index(DATE_COL).squeeze()
         # Converting the index as date
         KCB.index = pd.to_datetime(KCB .index)
         
         
    except Exception as e:
        err_msg = ('There was an error importing the file or extracting the '
                   'date or value column. Please check the configuration file'
                   'or input files')
        print(e,err_msg)
    
    # Create a daily pandas series from start to end date   
    # Fit in the data from the input file into the blank date series
    # Assume all dates where no data is KC= 0.0
    OUT = pd.Series(0,index= pd.date_range(START_DATE,END_DATE),name=VAL_COL,
                    dtype='float64')
    
    try:
        if OUT.shape < KCB.shape:
            err_msg= ('Number of dates in input file is greater than '
                   'number of dates between start and end date.'
                     )
            raise Exception(err_msg)
        else:
            ixs = OUT.index.intersection(KCB.index)
            OUT.loc[ixs] = KCB.loc[ixs]
        
    except Exception as e:
        
        err_msg = ('There was an error importing the file or extracting the '
                   'date or value column. Please check the configuration file '
                   'or input files')
        print(e,err_msg)
        
 
    #-----------------#
    # WRITE FORMATTED #
    #-----------------#
    
    try:
    
        sect_header = ''.join(['@DATE  KCB\n'])
        OUT.index = OUT.index.strftime('%y%j')
    
        FORM_DATA = OUT.to_string(header=False,
                index=True,
                float_format= '{:>2.2f}'.format
                )
        sect_values_n = ''
        for line in FORM_DATA.splitlines():
            line = line +'\n'
            sect_values_n += line 
        
        # Combine all strings
        o_text = HEADER_TEXT + sect_header + sect_values_n
        
        kcb_file = OUT_DIRECTORY.joinpath('KCB.CDE')    
        with open(kcb_file, 'w') as f:
            f.write(o_text)
        
        print('Program completed with no errors')
    
    except Exception as e:
        
        err_msg = ('There was an error writing the output file\n')
        print(err_msg,e)
    
   
    