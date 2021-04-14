# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: more basics
    
    (1) More advanced list operations
    (2) Types of logical conditions.
    (3) While loops
    (4) Nested for loops
    (5) Intro to functions
    
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
#import numpy as np

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

    
    # "List comprehension" (fancy term for filling in list in one line)
    list1 = [s for s in range(5)]
    print(list1)
        
    # Logical operators
    x = 1
    y = 2
    
    print(x == 1) # equal to (** has to be two equal signs)
    print(x>0)    # greater than
    print(x>=0)   # greater than equal to
    print(x!=0)   # not equal to
    
    for s in list1:
        if s < 3:
            print('%d is less than 3'%(s))
        else:
            pass
    
   
    # and: both conditions must be met to be == True
    # or:  either condition  can be met to be == True
    
    for s in list1:
        if s < 3 and s > 1:
            print('%d is less than 3 and greater than 1'%(s))
        else:
            pass
    
    for s in list1:
        if s < 3 or s > 1:
            print('%d is less than 3 or greater than 1'%(s))
        else:
            pass
    
    
    # Loop until condition is met; be careful. May cause infinite loop
    i = 0
    while i < 30: 
        print(i)
        i = i +1
        # If "i" did not increase, it would always be less than 30. Will never stop running
         
    
    i = 0
    while i < 30: 
        print(i)
        i+=1  # short cut notation for i= i+1
    
    
    # Nested for loops
    for i in range(30):
        for j in range(10):
            print(i,j)
    

#%%---------------------------------------------------------------------------#

    #
    # Python function
    #
    
    # must start with "def" e.g. define
    # followed by parenthesis ()
    def add_two_numbers(n,m):
        
        """ Description about your function"""
        
        # n and m are function arguments that are required
        
        return n + m
    
    print(add_two_numbers(1,3))
    
    # put the returned value into the variable res
    res = add_two_numbers(1,3)
    print(res)
    
    # Function requires no arguments
    def always_return_100():
        
        return 10*10
    
    print(always_return_100())
    
    # Returns error 
    print(always_return_100(5))
        
        
    
    
    
   