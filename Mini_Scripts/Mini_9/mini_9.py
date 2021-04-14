# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: Introduction to GDAL!
    
    Objective: Plot CDL raster map for eastern Kansas River basin (EKSRB) for
    all categories and only the corn category.
    
    https://gdal.org/tutorials/
    
    "GDAL is translator library for raster and vector geospatial data formats that is 
    released under an X/MIT style Open Source License by the Open Source 
    Geospatial Foundation"
    
    Here we are dealing with geolocated raster data (not shapefiles).
    
    Be careful working with rasters, large rasters can overlaod your RAM. Be 
    mindful of what you load in at a time. In addition, plotting can take time
    for large rasters. CDL is 30 m data so you may have to zoom to see on matplotlib
    I zoomed in for a small portion of the EKSRB.
    
    Packages: matplotlib, cartopy, numpy, and gdal
    
   
INPUTS:
    
    (1) Shapefiles in the directory
    (2) CDL RAster layer from 2008
    
OUTPUTS:
    
    (1) 

AUTHOR: Zachary Zambreski, Kansas State University (2020)


"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
#from matplotlib import colors,colorbar
from osgeo import gdal
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
    
    # Path to the boundary shapefile of the eastern Kansas River Basin
    boundary = './boundary_only.shp'
    counties = './boundary_counties.shp'
    
    # Path to CDL raster
    cdl = './CDL_KSriver_Watershed_2018.tif'
    
#%%---------------------------------------------------------------------------#
    
    #------------------------#
    # Import the raster data #
    #------------------------#
    
    #
    # We need to extract the values of the raster
    # WE then need to use the geotransform metadata to define a grid of lats and 
    # lons that correspond to each pixel location. 
    #
    
    # Open the raster in python using GDAL
    raster = gdal.Open(cdl)
    
    #
    # Learn some background about your raster
    # Check type of the variable 'raster'
    #
    print(type(raster),'\n')
  
    # Projection
    print('Projection: ',raster.GetProjection(),'\n')
    
    # Dimensions
    print('Raster x size: ',raster.RasterXSize,'\n')
    print('Raster y size: ',raster.RasterYSize,'\n')
    
    # Number of bands
    # There's only 1. It's not multidemnsional. Some rasters from satellite
    # data will contain multiple bands!
    print('Number of bands in the raster: ',raster.RasterCount,'\n')
    
    # Metadata for the raster dataset
    print('Metadata: ', raster.GetMetadata())
    
    gt   = raster.GetGeoTransform()
    proj = raster.GetProjection()
    
    # Numbers correspond to categories: crop types
    data = np.array(raster.ReadAsArray(),dtype=np.float)
    
    print('Geotransform: ',gt)
    
    # Tif rasters do not have coordinates for each pixel saved (unfortunately).
    # You have to derive them using the geotransform information such as the
    # top left corner, x and y resolution....
    # Corner corodinates and resolution
    
    xres = gt[1] # 30 meters
    yres = gt[5]
    # get the edge coordinates and add half the resolution
    # to go to center coordinates
    xmin = gt[0] + xres * 0.5
    xmax = gt[0] + (xres * raster.RasterXSize) - xres * 0.5
    ymin = gt[3] + (yres * raster.RasterYSize) + yres * 0.5
    ymax = gt[3] - yres * 0.5
    
    
    extent = (gt[0], gt[0] + raster.RasterXSize * gt[1],
              gt[3] + raster.RasterYSize * gt[5], gt[3])
    
    raster = None # Equivalent to closing a file 
    
    # Create a grid of xy coordinates in the original projection
    # These will be in meters. WE won't use this to plot, but it's important
    # to know. 
    xy_source = np.mgrid[xmin:xmax+xres:xres, ymax+yres:ymin:yres]
  
    
    # It's a rectangle!
    print('Shape of your raster: ',np.shape(data))    
    print('Shape of your xy_source: ',np.shape(xy_source))

#%%---------------------------------------------------------------------------#
    
    #------------------------#
    # Post process the array #
    #------------------------#
        
    # Post-process the array
    # Set values equal to 255 to nan.  (these are outside of the EKSRB)
    # I believe value in ArcGIS wheny you clip a raster tif 
    # We don't care about them and don't want them plotted as a color
    data[data==255] = None
    
    # Create a new array that only selects pixels with a value that is equal to
    # 1, which is corn
    corn = np.array((data == 1)*1,dtype=np.float64)
    corn[corn==0] = np.nan
    
#%%---------------------------------------------------------------------------#
   
    # Create figure axes
  
    
    # Add the cartopy object
    # Select projection
    # Here we are specifying projection parameters based on the source data.
    # Always check projection info on rasters or shapefile as it is important
    # to extract the location coordinates. If you don't specify the write 
    # projection for matplotlib, you wont' see anything plotted.
    # **Super important**
    prj = ccrs.AlbersEqualArea(central_longitude  = -96,
                               standard_parallels = (29.5,45.5),
                               central_latitude   = 23)
    
    
    # Defining axes different. Use subplot_key words (kw)
    fig,axes = plt.subplots(1,2,figsize=(8,3),subplot_kw={'projection': prj})
    
    #ax = plt.axes(projection = prj)
    
    def drawbasemap(ax):
        
        """ Standard basemap for each subplot """
    
        # Extent of the map in latitude and longitude. Here we can use latitude
        # and longitude rather than use meters, which would be yikes...
        # LEt's Zoom in!
        zoom = [-97.0, -94.4, 38.6,40]
        ax.set_extent(zoom)
    
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

    
    #--
    # Subplot 1 (all cateogries)
    #--
    
    ax = axes[0] # set the axes we want to draw on
    
    drawbasemap(ax)
    
    # Normalize colors between these two values
    # acre-feet averages 52 
    # Let's set from -15 to 15
    vmin = 0
    vmax = 200
    
    cmap = plt.cm.YlGnBu      # Choose sequential colormap 
    
    # Plot a color mesh grid
    gridLons = xy_source[0,:,:].T # Python does rows by columns!! T stands for transpose. Numpy method!
    gridLats = xy_source[1,:,:].T
    #img = ax.pcolormesh(gridLons, gridLats, data, transform = prj)  # MUCH SLOWER
    img = ax.imshow(data,extent=extent,vmin=vmin, vmax=vmax,)
    
    ax.set_title('All categories')
    
    #plt.colorbar()
        
    #--
    # Subplot 2 (only corn)
    #--
    
    ax = axes[1]   
    drawbasemap(ax)
    #img = ax.pcolormesh(gridLons, gridLats, corn, transform = prj)
    
    # You need to zoom in on this plot to see!!
    img = ax.imshow(corn,extent=extent,vmin=0,vmax=1,cmap=cmap)
    
    ax.set_title('Corn (ZOOM IN USING MAGNIFYING GLASS)')
    
    plt.subplots_adjust(wspace=0.3)
    
    # Change the default dpi: dots per inch! This is high resolution stuff!!!
    # Larger dpi, larger size file...beware!
    fig.savefig('./Fig_9.png',dpi = 500)
        
        
        
        
    
       
   
