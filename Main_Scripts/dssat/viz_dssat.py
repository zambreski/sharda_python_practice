# -*- coding: utf-8 -*-
"""

PURPOSE: Illustrate the power of Python using a DSSAT dataset. Create summary 
figures.   

INPUTS/REQUIREMENTS:
    
    (1) Directory containing ".OSU" files from Alabama simulations
    (2) Spreadsheet with observed yields from NASS
      
    
OUTPUTS:
    
    (1) Three figure types
 

AUTHOR: Zachary Zambreski, Kansas State University (2020)

"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

from __future__ import division
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#------#
# MAIN #
#------#

if __name__== "__main__":
    
    #--------#
    # INPUTS #
    #--------#
    
    # File directory with DSSAT output 
    inDir = '../SeasonalAnalysis'
    
    # File prefix for DSSAT output. Files are formatted "AL0181**.OSU". Consistent
    # file formmating will always make future coding MUCH easier.
    pref = 'AL0181'
    ext  = '.OSU'
    
    # NASS file name
    inNass = 'NASS_Obs.xlsx'

#%%---------------------------------------------------------------------------#
    
    #-----------------#
    # Data processing #
    #-----------------#
    
    #
    # Load DSSAT file into python/pandas dataframe
    # Create a new panel 
    #
    
    # Blank dataframe to store processed data
    outpd = pd.DataFrame()
    
    # Iterate each .OSU file using file format
    for s in range(1,38):

        try:
            # Load the .OSU file using fixed width
            # If column widths aren't provided,assumes white space is delimeter
            # Skip rows that are metadata
            inDSSAT = pd.read_fwf('%s/%s%02d%s'%(inDir,pref,s,ext),skiprows = 3)        
            
            # We only need one row for soil id since it is constant. Retrieve the
            # first index, which is 0. Python index always starts from 0. In Matlab,
            # indices start from 1. 
            soil_id       = inDSSAT['SOIL_ID...'].iloc[0] 
            harvest_yield = inDSSAT['HWAH']
        
            # Add yield for soil type as column
            outpd[soil_id] = harvest_yield
        except:
            pass
    
    # Print first couple of rows from dataframe
    print(outpd.head())
    
    # Save new panel before visualization. We can use this new file later to
    # accerlate post-simulation analysis
    outpd.to_excel('./yield_AL.xlsx')
    
    #
    # Load observed county yield from NASS 
    #
    
    # Load excel spreadsheet into pandas dataframe 
    inNASS = pd.read_excel('%s/%s'%(inDir,inNass))
    
    # Extract column in dataframe
    obsYield = inNASS['Yield']

#%%---------------------------------------------------------------------------#
    
    #------------#
    # Statistics #
    #------------#
    
    # Row mean (average yield over time across soils)
    # Using functions inherited within the Pandas Library as the dataframe
    # "outpd" is a pandas based object
    avg_yield_time = outpd.mean(axis=1)
    # Column mean (average yield by soil type)
    avg_yield_soil = outpd.mean(axis=0)
    
    # Calculate the RMSE for each soil type compared to observed data
    [nRows,nCols] = outpd.shape
    rmse = outpd.sub(obsYield, axis=0).pow(2).sum().divide(nRows).pow(0.5)
    
    # Alternative RMSE calculation
# =============================================================================
#     rmse = np.zeros((nCols))
#     for i in range(nCols):
#         sim = outpd.iloc[:,i]
#         rmse[i] = np.sqrt(np.sum(np.square(obsYield - sim))/nRows)
# =============================================================================
    
    print('Soil type with lowest RMSE: %s (%.2f kg/ha)'%(rmse.idxmin(),rmse.min()))
    print('Soil type with highest RMSE: %s (%.2f kg/ha)'%(rmse.idxmax(),rmse.max()))
    
    # Order RMSE by least to greatest
    rankRMSE = rmse.sort_values()
    

#%%---------------------------------------------------------------------------#
    
    #----------------#
    # Visualizations #
    #----------------#
    
    #
    # Figure 1
    # Plot average yield through time across soil types
    #
    
    # Initialize the plot and properties   
    # Figure size (figsize) in inches (e.g. 6" by 3")
    fig,ax = plt.subplots(1,1,figsize=(6, 3))
    font = {'family' : 'Arial',
            'weight' : 'normal',
            'size'   :11}
    plt.rc('font', **font)
    degree_sign = u'\N{DEGREE SIGN}'
    fig.patch.set_facecolor('white')
    
    # Plot the x,y data from simulated DSSAT mean
    x = avg_yield_time.index.values
    y = avg_yield_time
    ax.plot(x,y,color = "r",marker= '.',markerfacecolor = 'white',markersize=10,
            markeredgecolor = 'coral',label = 'DSSAT')
    
    # PLot data from NASS
    y = obsYield
    ax.plot(x,y,color = "k",marker= '.',markerfacecolor = 'white',markersize=10,
            markeredgecolor = 'gray',label = 'NASS')
    
    # Plot fine-tuning. Change options such as axis labels, colors, background 
    # colors, font style, etc. There are thousands of different settings in
    # order to improve the asethetics of your plot. You may spend hours fine 
    # tuning. Googling "python matplotlib" with your question will most likely
    # returnthe API documentation for how to code a task 
    # (e.g. "python matplotlib how to set figure title)
    ax.yaxis.grid(linewidth =1,linestyle=':',color='w')  
    ax.xaxis.grid(linewidth =1,linestyle=':',color='whitesmoke')  
    ax.set_facecolor('gainsboro')
    ax.set_xlabel('Year',fontweight='bold')
    ax.set_ylabel('Mean yield (kg/ha)',fontweight = 'bold')
    
    # legend
    ax.legend()
    
    # Change margins betewen subplots and the edges of figure
    plt.subplots_adjust(hspace= 0.30,bottom=0.15,top =0.95,wspace=0.35,left=0.15)
    
    # Save figure to current working directory
    fig.savefig('./figure_1.png')
    
    #
    # ** Figure 2 **
    # Bar plot of average yield by soil type
    #
    
    fig,ax = plt.subplots(1,1,figsize=(7, 3))
    font = {'family' : 'Arial',
            'weight' : 'normal',
            'size'   :11}
    plt.rc('font', **font)
    degree_sign = u'\N{DEGREE SIGN}'
    fig.patch.set_facecolor('white')
    
    # Pandas objects can also be directly called for plotting
    rankRMSE.plot.bar(color = 'coral',zorder=100)
    
    ax.set_ylabel('Root mean square error',fontweight = 'bold')
    ax.yaxis.grid(linewidth =1,linestyle=':',color='w')  
    ax.xaxis.grid(linewidth =1,linestyle=':',color='whitesmoke')  
    ax.set_facecolor('gainsboro')
    
    plt.subplots_adjust(hspace= 0.30,bottom=0.40,top =0.95,wspace=0.35,left=0.10)
    
    # Save figure to current working directory
    fig.savefig('./figure_2.png')
    
    #
    # Figures 
    # One-to-one plots between simulated yields and observed yields
    #
    
    def prettyPlot(ax):
        
        """ Make axis assume these settings 
        
        ax: Matplotlib axes
        
        
        """
        
        ax.set_facecolor('gainsboro')
        x = np.linspace(0,15000,100)
        y = x
        ax.plot(x, y, linestyle  = '-',color = 'darkgray',linewidth= 0.75)
        ax.set_xlim([1000,13000])
        ax.set_ylim([1000,13000])
        ax.yaxis.grid(linewidth =1,linestyle=':',color='w')  
        ax.xaxis.grid(linewidth =1,linestyle=':',color='whitesmoke')  
    
    soilIDs = outpd.columns
    nSoils  = len(soilIDs)
    
    # Iterate all soil IDs and create individual plots
    for i in range(nSoils):
        
        # Initialize the plot and properties   
        # Figure size (figsize) in inches (e.g. 6" by 3")
        fig,ax = plt.subplots(1,1,figsize=(5, 4))
        font = {'family' : 'Arial',
                'weight' : 'normal',
                'size'   :11}
        plt.rc('font', **font)
        degree_sign = u'\N{DEGREE SIGN}'
        fig.patch.set_facecolor('white')
        
        x = outpd.iloc[:,i] # simualted
        y = obsYield        
        ax.scatter(x,y,color ='gray',label = 'Yield',s = 10)
        
        # Fine-tuning
        prettyPlot(ax)
        ax.set_xlabel('Simulated yield (kg/ha)',fontweight='bold')
        ax.set_ylabel('Observed yield (kg/ha)',fontweight = 'bold')
        ax.text(2000,12000,"RMSE = %.1f"%(rmse[outpd.iloc[:,i].name]),ha='left')
        
        # Set title of plot to soil ID
        title = outpd.iloc[:,i].name
        ax.set_title(title,fontweight = 'bold')
        
        # Change margins betewen subplots and the edges of figure
        plt.subplots_adjust(hspace= 0.30,bottom=0.15,top =0.90,wspace=0.35,
                            left= 0.18)
     
        #fig.savefig('./Figure_3_%s.png'%(title))
        
        # Close the window, so 30+ windows don't open simulatenously
        plt.close()
        

