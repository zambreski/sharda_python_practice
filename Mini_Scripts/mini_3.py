# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: Introduction to numpy package
    
    Numpy: numerical python
    
    When you're working with arrays, numpy methods perform more efficiently
    than trying to work with lists. NumPy arrays are stored at one continuous
    place in memory unlike lists, so processes can access and manipulate them 
    efficiently.
    
    It also has functions for working in domain of linear algebra, 
    fourier transform, and matrices. V
    
    *Many* other packages depend on numpy!
    
    In climate science, we often work with gridded data (space and time). Numpy
    is a nice library that makes doing calculations easy. 
   
    
    
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

    print(type(np))
    print(np.__version__)
    
    # Initalize a blank/empty array
    a = np.array([])
    print(type(a)) #numpy array
    print(a)
    
    # Initalize array with 5 zeros
    b = np.zeros(5)
    print(b)
    
    c = np.ones(5)
    print(c)
    
    # Element-wise addition  
    d = b + c
    print(d)
    
    # Initalize nnumpy array with some known values
    list1 = [40,30,35,60]
    e = np.array(list1)
    
    # Indexing is similar to lists,dictionaries, other python objects...
    print(e[0])  # first
    print(e[-1]) # last
    
    # "Slicing" :
    print(e[:]) # : by itself means everyting ()
    print(e[:1]) # :1 up to but not including 2nd item (e.g. the first)
    print(e[:2]) # :2 up to but not including 3rrd item (e.g. the first)
    
    # Take the dot product of two arrays
    print(np.dot(c,d))
    
    # 2-day array
    a_2d = np.array(([1,2,3],[4,5,6])) # Added the inner parenthesis for 2-d 
    print(a_2d)
    print(a_2d.shape) # n rows by m columns (nrows,mcolsc)
    
    print(a_2d.mean(axis=0))
    print(a_2d.mean(axis=1))
    print(a_2d.mean())
    
    arr = np.array([[1,2,3,4,5], [6,7,8,9,10]])

    print('2nd element on 1st dim: ', a_2d[0, 1]) 
    
    # What do you think these built-in methods do?
    print(a_2d.std(axis=0))
    print(a_2d.std())
    
    # 3-d array
    # Perhaps lat x lon x time
    arr = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])
    print(arr) 
    print(arr.shape)   # attribute of arr
    print(arr.ndim)
    print(arr.dtype)
    print(arr[0,0,0])
    
    # Last item in every dimension
    print(arr[-1,-1,-1])
    
    # Take some slices
    print(arr[-1,:,:])

    
    
  