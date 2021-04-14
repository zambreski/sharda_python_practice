# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: Cartopy; More advanced mapping
    
    Objective: Plot SVI for the Eastern Kansas River Basin
    
    In this example, we have to specify a different projection because of 
    the source data (SVI).  
    
   
INPUTS:
    
    (1) Shapefiles in the directory
    
OUTPUTS:
    
    (1) None

AUTHOR: Zachary Zambreski, Kansas State University (2020)


"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
from matplotlib import colors,colorbar

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
    boundary = './boundary_only.shp'
    
    # This shapefile is in Albers Equal area!
    # I learned this from ArcGIS (right-click source)
    """false_northing:	0.00000000
    central_meridian:	-96.00000000
    standard_parallel_1:	29.50000000
    standard_parallel_2:	45.50000000
    latitude_of_origin:	37.50000000"""
    
    svi      = './KS_SVI.shp'
    
    
#%%---------------------------------------------------------------------------#
    
    # Create figure axes
    fig,axes = plt.subplots(1,1,figsize=(8,4.5))
    
    # Add the cartopy object
    # Select projection
    # Here we are specifying projection parameters based on the source data.
    # 'KS_SVI.shp' has Albers equal area projection with the following parameters
    # Important cause the units of the geometry object is in meters and not
    # latitude and longitude degrees.
    # This makes it slightly more cryptic to the brain in my opinion. 
    
    prj = ccrs.AlbersEqualArea(central_longitude = -96,
                               standard_parallels = (29.5,45),
                               central_latitude = 37.5)
    
    ax = plt.axes(projection = prj)
    
    # Extent of the map in latitude and longitude. Here we can use latitude
    # and longitude rather than use meters, which would be yikes...
    extent = [-94.3, -97.3, 38.6,40.01]
    ax.set_extent(extent)
    
    # Draw states using built-in shape features
    # First arguement is shapely geometry, second argument is crs
    ax.add_feature(cfeature.NaturalEarthFeature('cultural','admin_1_states_provinces_lines',
                                                '10m',edgecolor='gray', 
                                                facecolor='none'))
 
    # Add eastern KS RB shapefile boundary only
    ax.add_geometries(Reader(boundary).geometries(),ccrs.PlateCarree(),edgecolor='k',
                      facecolor='none')

    #
    # Color each shape based on the field 'SVI' in the attribute table
    #
    
    # Normalize colors between these two values
    # SVI ranges from -18 to 20
    # Let's set from -15 to 15
    vmin = -15
    vmax = 15
    
    cmap = plt.cm.RdBu      # Choose diverging colormap 
    
    # Iterate each shape in the shapefile
    # Determine its color based on value
    # Plot the shape to the map ax with the specified color
    for c,county in enumerate(Reader(svi).records()):
        
        # county.attributes returns a dictionary with all the fields
        # Using the field attribute 'SVI'
        value  = county.attributes['SVI']
        
        # Choose color based on value
        colorRGB  = cmap((value-vmin)/(vmax-vmin))[:3]
        # Add the shape to the axes
        ax.add_geometries([county.geometry], crs = prj,facecolor=colorRGB,
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
    cb.set_label('SVI',fontweight = 'bold')
    
    #
    # Map grid lines (lots of fine-tuning your map)
    #
# =============================================================================
#     gl = ax.gridlines(crs=prj, draw_labels=True,
#                   linewidth=0.5, color='gray', alpha=0.5, linestyle='--')
#     gl.xlabels_top = False
#     gl.ylabels_right = False
#     gl.xlines = True
#     gl.xlocator = mticker.FixedLocator([-94, -95, -96,-97,-98])
#     gl.ylocator = mticker.FixedLocator([38,39,40])
# =============================================================================
    
    plt.subplots_adjust(right=0.8)
    
    #fig.savefig('./Fig_7.png')
        
        
        
        
    
       
   
