# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: Introduction to pandas package
    
    Pandas: panel data
    
    Most popular Python package for doing data analysis.
    
    " Python package providing fast, flexible, and expressive data structures 
    designed to make working with “relational” or “labeled” data both easy and 
    intuitive. It aims to be the fundamental high-level building block for 
    doing practical, real world data analysis in Python."
    
    Two important data structures: series and data frame
    
    
    Link: https://pandas.pydata.org/docs/getting_started/overview.html
    
    
INPUTS:
    
    (1) None
    
OUTPUTS:
    
    (1) None

AUTHOR: Zachary Zambreski, Kansas State University (2020)

Created on Mon Dec  7 15:48:14 2020

"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

#from __future__ import division
#import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

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

#%%---------------------------------------------------------------------------#

    print(type(pd))
    
    #-----------------------------------#
    # Explore data structures in pandas #
    #-----------------------------------#
    
    # Create a pandas series data strcuture (specialized array...)
    # nan: not a number (e.g. null)
    s = pd.Series([1, 3, 5, np.nan, 6, 8])
    print(s)
    
    
    # Create a dataframe
    
    # First,Create a dictionary data structure and fill
    # Dictionary "keys" are the column names
    # Dictionary "values" are the data 
    input_data_dic = {'A': 1.,
   ...:               'B': pd.Timestamp('20130102'),
   ...:               'C': pd.Series(1, index=list(range(4)), dtype='float32'),
   ...:               'D': np.array([3] * 4, dtype = 'int32'),
   ...:               'E': pd.Categorical(["test", "train", "test", "train"]),
   ...:               'F': 'foo'}
    
    # Pass the dictionary to the pd.DataFrame object
    df1 = pd.DataFrame(input_data_dic)
    print(df1)
    
    # Returns the row index. We did not specifcy what the index was so it 
    # uses a default numbering (0,1,2,...)
    print(df1.index)
    # Column names 
    print(df1.columns)
    
    # Index the data frame
    # In pandas there are several ways to index the data frame
    
    # First way is by numbered index using method "iloc"
    print(df1.iloc[0,0])
    
    # Second method is using column name and index using "loc" method
    # Very useful when you don't know much about the ordering
    # [Row index, column index]; use brackets[]
    
    print(df1.loc[2,"E"])
    
    #########
    
    # Create a new dataframe
    
    input_data_dic = {'Year': np.array([1985,1968,1987,1988]),
   ...:               'yield': np.array([38,20,55,40]),
   ...:               'rain': np.array([400,500,450,300])}
    
    # Pass the dictionary to the pd.DataFrame object
    df2 = pd.DataFrame(input_data_dic)
    # Set the row index to 'Year'
    df2.set_index('Year',inplace=True) 
    #inplace arguments means to not create a new object. If you don't set this
    # the change will not be applied to the original object
    # Now we can use the year as the row index
    print(df2)
    print(df2.loc[1985,'yield'],df2.loc[1985,'rain'])
    
    # Get the column data for the yield
    print(df2['yield'])
    
    # Get both yield and rain. Notice the double brackets
    print(df2[['yield','rain']])
    
    
    # Create an empty dataframe
    df3 = pd.DataFrame()
    
    # Populate the dataframe column-by-column
    
    
    
    

    