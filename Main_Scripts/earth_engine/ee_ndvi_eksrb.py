# -*- coding: utf-8 -*-
"""

PURPOSE: Create a figure with two axes that show summer average NDVI for Eastern
    Kansas River Basin in 2012 vs. 2019. Backend will be performed on Google 
    Earth Engine servers
    
    Google Earth Engine has amazing functionality for processing earth-based 
    datasets, and the best part is that the brunt of the work is done on their
    side, not your machine. 
    
    Benefits: 
        We don't need to have these datasets on our machine. If you have
    not worked with satellite datasets, they are QUITE large. 
    
    Drawbacks:
        You are limited to how much you can use GEE for free. The more data crunching,
        the more resources required on the backend. Be mindful of this.
    
    README MORE About download:
        https://developers.google.com/earth-engine/guides/python_install-conda
        https://developers.google.com/earth-engine/guides/python_install

 
    
INPUTS:
    
    (1) EE URL
    (2) EE API KEY (your credentials)
    (3) Payload with data information
    
OUTPUTS:
    
    (1) 1 Figure, Two axes, each showing annual summer mean NDVI

AUTHOR: Zachary Zambreski


"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import ee
import geopandas as gpd

#------------------------#
# USER-DEFINED FUNCTIONS #
#------------------------#

def extractShp(ifile):
    
    """
    
    Extract the extent of a shapefile in a format that can be used by
    Google Earth Engine
    
    Parameters
    ----------
    ifile : String
        Path to shapefile

    Returns
    -------
    features : List
        List of EE features (in JSON)

    """
    
    
    shapefile = gpd.read_file(ifile)
    
    features = []
    for i in range(shapefile.shape[0]):
        geom = shapefile.iloc[i:i+1,:] 
        jsonDict = eval(geom.to_json()) 
        geojsonDict = jsonDict['features'][0] 
        features.append(ee.Feature(geojsonDict)) 
    
    return features

#------#
# MAIN #
#------#

if __name__== "__main__":
    
    #--------#
    # INPUTS #
    #--------#
    
    # 2012 was a drought year
    years     = [2012,2019]
    startDate = [6,1]     # month/day
    endDate   = [8,31]    # month/day
    
    # Earth Engine dataset to use
    ee_dataset = "MODIS/006/MOD13A1"
    # resolution of the output image we want (meters). EE can upscale/downscale if
    # different from original source
    res = 500 #meters
    
    
    # File prefix of output raster
    oName = 'NDVI_'
    
    # Path to EKSRB shapefile
    shpFile= './shapefiles/EKSRB.shp'

#%%---------------------------------------------------------------------------#
    
    #-------------------------#
    # Google Earth Processing #
    #-------------------------#
    
    # Iterate years
    for year in years:
        
        print('Processing %d'%(year))
        
        # Format start and end dates that EE likes
        sDate = '{}-{:02d}-{:02}'.format(year,startDate[0],startDate[1])
        eDate = '{}-{:02d}-{:02}'.format(year,endDate[0],endDate[1])
        
        # Initialize the Earth Engine module.
        # It will tell you that you need to authenticate if it's your first time
        # Just follow the instructions on your screen. Type the command in your 
        # anaconda prompt terminal window
        # Once you do this, you will have access to all the back-end functionality
        ee.Initialize()
        
        # Load collection of available iamges across the dates
        dataset = ee.ImageCollection(ee_dataset).filter(ee.Filter.date(sDate, eDate));
        # Select NDVI band
        ndvi_coll = dataset.select('NDVI');
        
        # Calculate the mean NDVI
        ndvi_mean =  ndvi_coll.reduce(ee.Reducer.mean());
        
        # Upload the shapefile into google Earth Engine
        features = extractShp(shpFile)
        fc = ee.FeatureCollection(features)
        geometry = fc.geometry()
        
        # Create a geometry representing an export region. This is just a basic
        # rectangle
        #geometry = ee.Geometry.Rectangle([-96, 38.8412, -94, 40.01236]);
        # Export excel table to your google drive. This is YOUR drive. Not Zach's.
        task = ee.batch.Export.image.toDrive(image=ndvi_mean, 
                                         description ='export_%d'%(year),
                                         fileFormat = 'GeoTIFF',
                                         region = geometry,
                                         scale = res,   
                                         # scale: resolution you want(meters).. Always specifiy 
                                         # resolution or it will make it coarse by defualt
                                         fileNamePrefix= oName + '%d'%(year))
        
        # Start the above task, which is export command. This task may take
        # some time. 
        task.start()
        
        # Check the status of the task, it may say "RUNNING" for status. Keep printing
        # until it says completed for the state key. This command returns a python
        # dictionary.
        task.status()
    
    # Go check your google drive to make sure the files are there!!!
    # download them to this directory. They will be used to create visualizations
    # I have already put the two downloaded files from my drive

#%%--------------------------------------------------------------------------#

    # ASSUMES YOU HAVE DOWNLOADED the two geotiffs to your computer in the
    # ./rasters folder
    
    #----------------#
    # Visualizations #
    #----------------#
    
    import cartopy.crs as ccrs
    from cartopy.io.shapereader import Reader
    import cartopy.feature as cfeature
    from osgeo import gdal
    import matplotlib.pyplot as plt
    import numpy as np
    
    # Raster paths
    inFiles  = ['./rasters/%s%d.tif'%(oName,year) for year in years]
    
    # Define projection
    prj = ccrs.PlateCarree()
    
    # Initalize matplotlib figure with the projection
    fig,axes = plt.subplots(nrows=1,ncols=2,figsize=(8,3),subplot_kw={'projection': prj})
    font = {'family' : 'Arial',
            'weight' : 'normal',
            'size'   :18}
    plt.rc('font', **font)
    
    # Choose sequential colormap to draw colors from
    cmap = plt.cm.RdYlGn
    
    # Normalize colors between these two values
    vmin = -0.5
    vmax = 1
    
    def drawbasemap(ax):
        
        """ Standard basemap for each subplot """
    
        # Extent of the map in latitude and longitude. Here we can use latitude
        # and longitude rather than use meters, which would be yikes...
        # LEt's Zoom in!
        zoom = [-97.0, -94.4, 38.6,40.1]
        ax.set_extent(zoom)
    
        # Draw states using built-in shape features
        # First arguement is shapely geometry, second argument is crs
        ax.add_feature(cfeature.NaturalEarthFeature('cultural','admin_1_states_provinces_lines',
                                                    '10m',edgecolor='gray', 
                                                    facecolor='none',zorder=100))
        
        # Add eastern KS RB shapefile boundary only
        ax.add_geometries(Reader(shpFile).geometries(),ccrs.PlateCarree(),
                          edgecolor='k',facecolor='none')
        
    
    # Iterate the files/open them/plot them
    for i,f in enumerate(inFiles):
    
        # Open the raster in python using GDAL
        raster = gdal.Open(f)
        
        #
        # Learn some background about your raster
        # Check type of the variable 'raster'
        #
        print(type(raster),'\n')

        # Dimensions
        print('Raster x size: ',raster.RasterXSize,'\n')
        print('Raster y size: ',raster.RasterYSize,'\n')
        
        # Number of bands
        # There's only 1. It's not multidemnsional. Some rasters from satellite
        # data will contain multiple bands!
        print('Number of bands in the raster: ',raster.RasterCount,'\n')
     
        gt   = raster.GetGeoTransform()
        #proj = raster.GetProjection()
        
        # Actual data (NDVI)
        data = np.array(raster.ReadAsArray(),dtype=np.float)/10000
    
        # Tif rasters do not have coordinates for each pixel saved (unfortunately).
        # You have to derive them using the geotransform information such as the
        # top left corner, x and y resolution....
        # Corner corodinates and resolution
        
        xres = gt[1] # 500 meters: based on our download option
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
        
        # Specify axes
        ax = axes[i]
        
        # Draw basemap options
        drawbasemap(ax)
    
        # Plot the raster using imshow
        img = ax.imshow(data,extent=extent, origin='upper',vmin=vmin,cmap=cmap,
                        vmax=vmax)
        
        ax.set_title('%d'%(years[i]),fontweight = 'bold')
    
    #
    # Create a colorbar below the two axes by creating a new axes
    #
    
    # Create new axes [x,y,width,height]
    cax = fig.add_axes([0.30, 0.20, 0.4, 0.04])
    cb1 = plt.colorbar(img,cax = cax,orientation='horizontal')
    cb1.ax.tick_params(labelsize=12)
    cb1.set_label('NDVI',color = 'k', fontweight = 'bold',labelpad = 5)
    for label in cb1.ax.xaxis.get_ticklabels()[1::2]:
        label.set_visible(False)
    
    plt.subplots_adjust(bottom=0.25)
    
    fig.savefig('./eksrb_ndvi.png',dpi=1000)