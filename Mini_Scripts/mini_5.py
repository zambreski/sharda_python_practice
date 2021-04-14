# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: Introduction to matlplib package
    
    
    Link:
    
    
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
import matplotlib.pyplot as plt
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
    # (1)
    
    # Creat some data to plot
    # Pandas Dataframe from mini- lesson 4
    # Now we are using multiple packages (e.g. pandas, numpy)
    input_data_dic = {'Year': np.array([1985,1986,1987,1988]),
                 'yield': np.array([38,20,55,40]),
                 'rain': np.array([400,500,450,300])}
    
    # Pass the dictionary to the pd.DataFrame object
    df = pd.DataFrame(input_data_dic)
    # Set the row index to 'Year'
    df.set_index('Year',inplace=True) 
    
    ##
    
    # Create blank figure window
    plt.figure()
    # Plot yield from pandas dataframe.
    # If only 1 array is provided, it assumes the x-axis is just the index
    # In this example, the index is actually year based on the pandas dataframe
    plt.plot(df['yield'])
    
    # Close the current figure window
    plt.close()
    
    # Create blank figure window
    plt.figure()
    a = np.array([100,200,300,250])
    # Here is there is no defined index, so it starts at 0 then 1,2,...
    plt.plot(a)
    
    ##
    
    # Create a figure window but explictly assign it to an object
    fig = plt.figure()
    plt.plot(df['yield'])
    plt.close(fig) # specify which figure to cose

#%%---------------------------------------------------------------------------#

    # (2)    

    #----------#
    # Subplots #
    #----------#
    
    # Create a figure with subplots
    # nrows x bycols (e.g. 1 row by 2 columns)
    # In this case, there are two objects: one for the entire window 
    # and one for each subplot axes
    fig,axes = plt.subplots(1,2)
    
    print(np.shape(axes)) # equals 2
    
    # Plot on the first axes
    # Use indexing of the axes
    axes[0].plot(df['yield'])
    
    # Plot on the second axes
    axes[1].plot(df['rain'])
    
    plt.close(fig)
    
    #
    # 2 x 2 subplots
    #
    
    fig,axes = plt.subplots(2,2)
    
    print(np.shape(axes)) # equals (2,2)
    
    axes[0,0].plot(df['yield'])
    axes[0,1].plot(df['rain'])
    axes[1,0].plot([1,2,3,4,5])
    axes[1,1].plot(np.arange(10))
    
    plt.close(fig)

#%%---------------------------------------------------------------------------#
    # (3)
    
    #----------------------------#
    # Fine-tuning with arguments #
    #----------------------------#
    
    # Matplotlib objects have tens to hundreds of optional argumenents that
    # can be used to alter the appearance of your figure and axes
    # IT usually takes some experimenting to determine what ultimately looks
    # good to your eyes. 
    
    # Consult the online documentation 
    # Can also use built-in "help" function
       
    fig,axes = plt.subplots(1,1)
    print(np.shape(axes)) # equals (. Only single subplot
    
    # Change the line to blue
    axes.plot(df['yield'],color='blue',label='yield')
    
    # Creates a legend using the "label" arguement passed to the axes
    axes.legend()
    
    # Axes text-labels
    axes.set_xlabel('Year')
    axes.set_ylabel('Yield')


#%%---------------------------------------------------------------------------#
    # (4)
    
    #-------------#
    # Scatterplots #
    #-------------# 
    
    # Create some data
    simYield = np.array([38,50,89,90,85,72,96,23])
    obsYield = np.array([30,53,80,70,96,80,95,40])
    
    # Create a group variable (e.g. soil type)
    # Has to equal dimensions of x and 
    
    # Four groups, corresponding to integers
    soilTypes = np.array([0,0,1,1,2,2,3,3])
    
    print('Number of unique groups: %d'%(np.unique(soilTypes).shape))
    
    fig,axes = plt.subplots(1,1)
    
    # c stands for color but if you provide groups, it will plot each group
    # the same color
    axes.scatter(simYield,obsYield,c=soilTypes)
    
    # Axes text-labels
    axes.set_xlabel('Simulated yield')
    axes.set_ylabel('Observed yield')
    
    plt.close(fig)
    
    #
    # Alternativly, use different marker symbols for each group
    #
    
    fig,axes = plt.subplots(1,1)
    
    # Scatter each group 1 at a time
    
    symb = ['^','+','.','o'] # 4 groups
    for s in range(len(symb)):
        axes.scatter(simYield[soilTypes == s],obsYield[soilTypes == s],
                     marker=symb[s])
    
    # Axes text-labels
    axes.set_xlabel('Simulated yield')
    axes.set_ylabel('Observed yield')
 
#%%---------------------------------------------------------------------------#
    # (5)
    
    #-----------#
    # Histogram #
    #-----------#    
    
    # Create random sample of size 1000
    # from normal distribution with mean 0 and standard deviation 3
    rs_n = np.random.normal(loc=0, scale=3,size=1000)
    print(len(rs_n))
    
    fig,axes = plt.subplots(1,1)
    
    # Histogram object in matplotlib
    axes.hist(rs_n,color = 'lightgreen',edgecolor = 'gray') 
    axes.set_xlabel('x')
    axes.set_ylabel('Frequency')
    
#%%---------------------------------------------------------------------------#
    # (6)
    
    #-------------------------------------------#
    # Create polygons and assign them to colors #
    #-------------------------------------------#
    
    # This logic is the same that will be used when filling in polygons such 
    # as Kansas counties...
    
    # There are probably hundreds approaches to this task
    # only showing one
    
    # Imported additional packages methods from matplotlib
    from shapely.geometry.polygon import Polygon
    from matplotlib.collections import PatchCollection
    from matplotlib import cm
    from descartes import PolygonPatch
    from matplotlib import colors,colorbar
    
    fig,axes = plt.subplots(1,1)
    
    # Add a weird shape polygon
    # Use coordinates for the polygon
    ring_mixed = Polygon([(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 0.8), (0, 0)])
    
    # Add it as a patch object. This is where you apply aesethic arguments such
    # as color, edge color, etc...
    patch1 = PolygonPatch(ring_mixed,color='coral' )
    
    # Add the patch to the axes
    axes.add_patch(patch1)
    
    # Add a rectangle
    rect1 = Polygon([(3, 1), (3, 3), (9, 3),(9,1),(3,1)])    
    patch2 = PolygonPatch(rect1,color='lightblue' )
    
    axes.add_patch(patch2)
    
    axes.set_xlim([0,10])
    axes.set_ylim([-1,5])
    
    #
    # Now lets say each polygon has some associated field or value that
    # should dictate its color...(e.g. yield)
    # This same logic would be used if we had polygons, for lets say...counties
    #
    
    # Dictionary
    data = {'county_1':38,'county_2':45}
    
    fig,axes = plt.subplots(1,1)
    
    # Create a colormap object    
    # https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html 
    cmap = plt.cm.RdYlBu   
    
    # Normalize colors between these two values
    vmin = 35
    vmax = 50
    
    def colorPolygon(y,poly):
        
        """ Function that colors a polygon based on input value y """
        
        # Use the colormap object to extract colors based on noramlized set of values
        colorRGB  = cmap((y-vmin)/(vmax-vmin))[:3]
        patch1    = PolygonPatch(poly,color=colorRGB )
        axes.add_patch(patch1)
    
    colorPolygon(data['county_1'],ring_mixed)
    colorPolygon(data['county_2'],rect1)
       
    axes.set_xlim([0,10])
    axes.set_ylim([-1,5])
    
    # Create a colorbar
    # Create a new axes on the figure [x,y,width,height]
    axCB = fig.add_axes([0.87, 0.17, 0.04, 0.56])
    norm = colors.Normalize(vmin=vmin, vmax = vmax)
    cb   = colorbar.ColorbarBase(ax= axCB, cmap  =cmap,
                                norm = norm,
                                spacing='uniform',
                                orientation='vertical'
                                )
    cb.set_label('Yield')
    
    plt.subplots_adjust(right=0.85)
    

       
    
   

    
        
    

    