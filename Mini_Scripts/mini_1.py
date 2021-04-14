# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: basics
    
    (1) Show python mathematical operators 
    (2) String formmating examples
    (3) Lists and list methods
    (4) Dictionaries
    (5) Typles
    (6) Boolean data types
    (7) If/else statements 
    (8) logical conditions
    
    
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
    
    #
    # Math operators
    #
    
    x = 10
    y = 15
    z = x*y
    
    print('x times y')
    print(x*y)
    
    print('x divided by y')
    print(x/y)
    
    print('%d * %d = %d'%(x,y,z))
    print('%d + %d = %d'%(x,y,x+y))
    
    # Show x-squared 
    print('%d^2 = %d'%(x,x**2))
    # Show x-cubed 
    print('%d^3 = %d'%(x,x**3))
    # Show square root of x
    print('sqrt(%d) = %.2f'%(x,x**0.5))
    
    # Float and integer mix
    x = 3.598
    y = 5
    z = x*y
    
    # type is a built-in function that tells you what data type something is
    # very helpful if you don't know or forget
    print(type(x))
    print(type(y))
    print(type(z))
    
    # %d: format integer
    # %s: format string
    # %f: format float
    
    print('%d * %d = %d'%(x,y,z))
    
    # What's the difference?
    print('%d * %d = %f'%(x,y,z))
    print('%d * %d = %.1f'%(x,y,z))
    print('%d * %d = %.3f'%(x,y,z))

# The line below begins a "cell" #%%
#%%---------------------------------------------------------------------------#
    
#
    # Show some list methods
    #
    
    list1 = [1,2,3,4] # lists are objects: contain data and code(e.g. methods)
    list2 = [8,7,10]
    
    print(list1)
    list1.append(9)
    print(list1)
    
    # Extends one list by another (e.g. combine lists to the first)
    list1.extend(list2)
    print(list1)
    
    list3 = []
    
    #
    # Built-in functions
    #
    
    # Range
    print(range(5))
    # Use built-in "list" to see innards
    print(list(range(5))) 
    # len is builit-in for "length"
    print(len(list(range(5))))
    print(len([5]))
    print(len(5))               # Returns error. Why?
    print(len('Hi Anish'))      # what did this do on a string?
    
    # Anything contained in the for loop needs to be indented
    for i in range(20):
        print(i)
        list3.append(i)
    print(list3)
    
    # Indexing (PYTHON BEGINS AT 0; Not 1!!!!!!!!!!!)
    
    print('First item in list: %d'%(list3[0]))
    print('Second item in list: %d'%(list3[1]))
    
    print('Last item in list: %d'%(list3[19]))
    print('Last item in list: %d'%(list3[len(list3)-1]))
    
    # Re-assign the first item in list1 to different value
    list1[0] = 10000
    print(list1)
    
    # NEgative index = backward index
    # -1 is always the last
    # -2 is second to last 
    # and so on..... Helpful for concise and when unknown lengths
    print('Last item in list: %d'%(list3[-1]))
    
    # List of different types
    list4 = ['hi',9,8.5,'DSSAT']
    for blah in list4:
        print(blah)
    
    # Remove (pop) item in the 0 index position
    print(list4)
    list4.pop(0)
    print(list4)
    
    # List of lists!!!
    list5 = [[1,2,34],[1,3,4,5,6,7],[1]]
    
    #
    # Dictionary
    #
    
    d = {'Zach': [1,2,3],'Anish':[5,6,7],'Jackson':[8,9,10]}
    print(d)
    print(d['Zach']) # 'Zach' is a key
    
    # Dictionary methods examples. See what they do!
    print(d.keys())
    print(d.values())
    
    # Iterate the keys in for loop
    for key in d.keys():
        print(key)
        print(d[key])
        
    #
    # Tuples
    #
    
    # Tuples look like lists but they use parenthesis ()
    # Big difference betweeen lists and dictionaries is that tuples are
    # "IMMUTABLE". That is, once they are defined,you cant change them
    # These object types are used when you want to create something that 
    # should never change or be altered in the future. Python will throw an
    # error. I don't see this data structure used that often
    
    tup1 = (1,2,3,4)
    print(tup1[0])
    
    # Run the below line and look at the error
    # Attempt to reassign first index to another value (remember, immutable!!) 
    tup1[0] = 1000
 
#%%---------------------------------------------------------------------------#
        
    #
    # Boolean and if-statements/ logical operators
    #
    
    x = 5
    y = 10
    
    multiply = True
    
    if multiply == True:
        print(x*y)
    else:
        pass
    
    # More concise 
    if multiply:
        print(x*y)
    else:
        pass
    
    if x*y == 50:
        print('x times y does == 50! yay')
    
    multiply = False    
    
    if multiply:
        print(x*y)
    else:
        print('Not performing multiplication')
