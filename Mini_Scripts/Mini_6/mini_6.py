# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: Introduction to matlplib package toolkit:cartopy
    
    Objective: Plot a map of Eastern Kansas River Basin (EKSRB) with counties.
    Fill in the counties with a color.
    
    README:
    
    You may need to install "cartopy" (follow steps for installing package). 
    Be careful about package warnings. 
    
    **If you run into package specific errors,please let email/slack me.** 
    
    
    I have previously used the "basemap" library for drawing maps in Python, but
    the basemap package has been deprecated since 2013, and it is recommended
    to use cartopy for map plotting purposes. I have used basemap in the past because
    it is what I originally learned and it's hard sometimes to try something 
    new...
    
    
    You will notice that packages considered deprecated have interesting errors
    outside of your general control. These are due to the fact that Python
    language continues to evolve in addition to package dependcies.
    
INPUTS:
    
    (1) Shapefiles in the directory
    
        boundary_only       (Exterior boundary of EKSRB)
        boundary_counties   (Counties clipped by the EKSRB)
    
OUTPUTS:
    
    (1) Map of Kansas

AUTHOR: Zachary Zambreski, Kansas State University (2020)


"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

#from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
from matplotlib import colors,colorbar
import matplotlib.ticker as mticker

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
    
    # Location to the boundary shapefile of the eastern Kansas River Basin
    # Remeber, the dot "." indicates a *relative path* on your computer
    # one dot ./   : current directory
    # two dots ../ : parent directory (one above the current)
    
    boundary = './boundary_only.shp'
    # County shapefile
    counties = './boundary_counties.shp'
    
    
#%%---------------------------------------------------------------------------#
    
    # Create figure axes
    fig= plt.figure(figsize=(7,3.5))
    
    # Declare an axes using a projection argument. Indicates the plot is in
    # mapping coordinates instead of normal x-y
    # Declaring add 1 row,1 col, get the 1 axes (only 1 in this example)
    ax = fig.add_subplot(1,1,1,projection=ccrs.PlateCarree())
    # Extent of the map in latitude and longitude
    extent = [-94, -97.5, 38.5,40.1]
    ax.set_extent(extent)
    
    # Draw states using built-in shape features
    # First arguement is shapely geometry, second argument is crs
    # You will notice that the shape is "coarse"
    ax.add_feature(cfeature.NaturalEarthFeature('cultural','admin_1_states_provinces_lines',
                                                '10m',edgecolor='gray', 
                                                facecolor='none'))
    
    # Add the counties in the eastern Kansas River Basin
    # First arguement is shapely geometry, second argument is crs
    ax.add_geometries(Reader(counties).geometries(),ccrs.PlateCarree(),
                      edgecolor='gray',facecolor='none')
    
    # Add eastern KS RB shapefile boundary only
    ax.add_geometries(Reader(boundary).geometries(),ccrs.PlateCarree(),edgecolor='k',
                      facecolor='none')
    
    #plt.close()
    
    for c,county in enumerate(Reader(counties).geometries()):
        print(c,type(county))
        
    # Let's color each county based on some attribute
    # Let's just use ascending integers from 0 to 16 (total of 17 counties)
    # So the counties will receive a color based on the order of position 
    # within the shape file. This is arbitrary. 
    
    values = np.arange(17)
    
    # Normalize colors between these two values
    vmin = 0
    vmax = 17
    cmap = plt.cm.RdYlBu     # Python colormap (Red-Yellow-Blue)
    
    # Iterate each shape in the shapefile
    # Determine its color based on value
    # Plot the shape to the map ax with the specified color
    for c,county in enumerate(Reader(counties).records()):
        
        # Choose color based on value
        colorRGB  = cmap((c-vmin)/(vmax-vmin))[:3]
        # Add the shape to the axes
        # county.geometry is an object that contains the x/y coordinates.
        ax.add_geometries([county.geometry], ccrs.PlateCarree(),facecolor = colorRGB,
                          edgecolor = 'gray',linewidth=0.5)
    
    
    # Create a colorbar
    # Create a new axes on the figure [x,y,width,height]
    # Change these settings to move its position or changes its size
    axCB = fig.add_axes([0.85, 0.20, 0.04, 0.56])
    norm = colors.Normalize(vmin=vmin, vmax = vmax)
    cb   = colorbar.ColorbarBase(ax=axCB, cmap  =cmap,
                                norm = norm,
                                spacing='uniform',
                                orientation='vertical'
                                )
    cb.set_label('Index',fontweight = 'bold')
    
    #
    # Map grid lines (lots of fine-tuning your map)
    #
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
    gl.xlabels_top = False
    gl.ylabels_right = False
    gl.xlines = True
    gl.xlocator = mticker.FixedLocator([-94, -95, -96,-97,-98])
    gl.ylocator = mticker.FixedLocator([38,39,40])
    
    plt.subplots_adjust(right=0.8)
    
    fig.savefig('./fig_6.png')
        
        
        
        
    
       
   
