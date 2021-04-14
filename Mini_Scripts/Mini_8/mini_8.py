# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: Cartopy; More advanced mapping
    
    Objective: Plot acre-feet of water used for points in the eastern Kansas 
    River basin
    
    Involves specifying a different projection because of the source data 
    
   
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
    counties = './boundary_counties.shp'
    
    # This shapefile is in NAD_1983_UTM_Zone_14N
    # I learned this from ArcGIS (right-click source)
    
    wuse      = './ks_watershed_wuse.shp'
    
#%%---------------------------------------------------------------------------#
    
    # Create figure axes
    fig,axes = plt.subplots(1,1,figsize=(6,4.5))
    
    # Add the cartopy object
    # Select projection
    # Here we are specifying projection parameters based on the source data.
    prj = ccrs.UTM(zone=14)
    
    ax = plt.axes(projection = prj)
    
    # Extent of the map in latitude and longitude. Here we can use latitude
    # and longitude rather than use meters, which would be yikes...
    # LEt's Zoom in!
    extent = [-95.0, -96.3, 38.75,39.6]
    ax.set_extent(extent)
    
    # Draw states using built-in shape features
    # First arguement is shapely geometry, second argument is crs
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

    #
    # Color each shape based on the field 'SVI' in the attribute table
    #
    
    # Normalize colors between these two values
    # acre-feet averages 52 
    # Let's set from -15 to 15
    vmin = 0
    vmax = 100
    
    cmap = plt.cm.YlGnBu      # Choose sequential colormap 
    
    # Iterate each point shape in the shapefile (e.g. a well)
    # Determine its color based on value
    # Put the information on lat/lon/color into lists
    
    colorL = [];lons = [];lats = []
    for c,well in enumerate(Reader(wuse).records()):
        
        # well.attributes returns a dictionary with all the fields
        # Using the field attribute 'SVI'
        value = well.attributes['Af_used_19']
        
        if value  == 0: # Ignore wells with zero, just clutter our map
            pass
        else:
      
            # Choose color based on value
            colorL.append(cmap((value-vmin)/(vmax-vmin))[:3])
            
            # Add the shape to the axes
            lons.append(well.geometry.coords.xy[0][0])
            lats.append(well.geometry.coords.xy[1][0])
    
    # Perform the plot command outside of the loop for "scatter". Much faster
    # than doing a scatter for each individual point
    ax.scatter(x = lons,y =lats,color=colorL, s = 10 ,transform = prj,
               edgecolor = 'k',linewidth = 0.25)

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
    cb.set_label('AF in 2019',fontweight = 'bold')
    
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
    
    fig.savefig('./Fig_8.png')
        
        
        
        
    
       
   
