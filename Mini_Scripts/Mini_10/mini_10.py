# -*- coding: utf-8 -*-
"""

PURPOSE: Python tutorial: Introduction to Statsmodels package
    
    
    Objective: Fit a lienar model between yield at harvest and preciptiation
    for one soil DSSAT output for Alabama. 
    
    https://www.statsmodels.org/stable/index.html
    
    Statsmodels is an "R" equivalent package that does a lot of the same
    statistical processing as R although more statisticans develop using R. 
    
   
INPUTS:
    
    (1) AL018102.OSU
    
    
OUTPUTS:
    
    (1) Linear model summary
    (2) Model assumptions check

AUTHOR: Zachary Zambreski, Kansas State University (2020)


"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import pandas as pd
import scipy.stats as stats

#------------------------#
# USER-DEFINED FUNCTIONS #
#------------------------#

def prettyplot(ax):
    
    """ Set a maplotlib axes with the following settings """

    ax.set_facecolor((254/256,246/256,230/256))
    ax.yaxis.grid(linewidth =1.,linestyle='-',color='gainsboro',zorder=0)

#------#
# MAIN #
#------#

if __name__== "__main__":
    
    #--------#
    # INPUTS #
    #--------#
    
    # Path to input file
    inFile = './AL018102.OSU'
  
#%%---------------------------------------------------------------------------#
    
    #-------------#
    # Import data #
    #-------------#
    
    # Load the .OSU file using fixed width [PANDAS]
    # If column widths aren't provided,assumes white space is delimeter
    # Skip rows that are metadata
    inDSSAT = pd.read_fwf('%s'%(inFile),skiprows = 3)       
    
    print(inDSSAT.columns)

#%%---------------------------------------------------------------------------#
    
    #----------------------#
    # Exploratory analysis #
    #----------------------#
    
    print('Number of observations: %d'%(inDSSAT.shape[0]))
    
    fig,axes = plt.subplots(1,2,figsize=(7, 3))
    
    # Before fitting the model...
    # Examine relationship between x and y
    # Let's explore relationship between preciptiation and yield
    #
    
    axes[0].scatter(inDSSAT['PRCP'],inDSSAT['HWAH'],zorder=100,color='coral',
                    edgecolor='gray')
    axes[0].set_xlabel('Precip (mm)')
    axes[0].set_ylabel('Yield (kg/ha)')
    prettyplot(axes[0])
    
    # Histogram of response variable
    axes[1].hist(inDSSAT['HWAH'],zorder=100,color='aquamarine',edgecolor='gray')
    prettyplot(axes[1])
    axes[1].set_xlabel('Yield (kg/ha)')
    axes[1].set_ylabel('Frequency')
    
    plt.subplots_adjust(bottom=0.15,left = 0.15,wspace=0.3)

#%%---------------------------------------------------------------------------#
    
    #----------------------------------------#
    # Modeling: Ordinary Least squares (OLS) #
    #----------------------------------------#
    
    # Fit the linear object model!
    # You pass the equation to fit as a string! (Y ~ x1 + x2 .... ) The "~" is
    # an equal sign. Same syntax as R
    # Results is an object! It has lots of data inside    
    # If you pass a pandas dataframe with column names, you can use those names
    # directly!
    results = smf.ols('HWAH ~ PRCP ', data = inDSSAT).fit()
    
    # Print summary output as text
    print(results.summary())
    
    print('R-squared: %.2f'%(results.rsquared))
    print('Adjusted R-squared: %.2f'%(results.rsquared_adj))
    
    # Get the values of your coefficients for each independent variable in 
    # your model (The betas in Y = b0 + b1*X1 + b2*X2....)
    # stored in "".params!
    print(results.params)
    print('Coefficient for precip: %.2f  yield / mm'%(results.params['PRCP']))
    
    # Fit evaluation
    residuals    = results.resid # (Y- Yhat) 
    rmse = np.sqrt(np.sum(np.square(residuals))/len(residuals))
    print('Model rmse: %.3f'%(rmse))
    
    fittedValues = results.fittedvalues
  
    
#%%---------------------------------------------------------------------------#
    
    #------------------------#
    # Diagnostic model plots #
    #------------------------#
  
    # 2 x 2 figure
    fig,axes = plt.subplots(2,2,figsize=(8,6))
    
    # (Subplot 1)
    # Plot between fitted HAWH and observed HAWH
    # A perfect model will fall on a straight one-to-one line
    #
    axes[0,0].scatter(fittedValues,inDSSAT['HWAH'],s = 5, color = 'gray')
    axes[0,0].set_ylabel('Fitted value', fontweight = 'bold')
    axes[0,0].set_xlabel('Observed', fontweight = 'bold')
    
    # Plot a one-to-one reference line
    x = np.linspace(5000,12000,100) 
    y = x
    axes[0,0].plot(x, y, linestyle  = '-',color = 'k',linewidth=1 )
    
    axes[0,0].text(10000,1000,"RMSE = %.2f\nR$\mathregular{^{2}}$ = %.2f"%(rmse,
                                                    results.rsquared),ha='center',
                                                    fontsize = 10)
    
    axes[0,0].set_xlim([5000,12000])
    
    prettyplot(axes[0,0])
    
    # (Subplot 2)
    # Scatterplot of residuals vs fitted values
    # The points should look random with no pattern
    # Patterns may indicate non-constant variance (heteroskedatsicty), which
    # is a violation of one of the underlying assumptions of linear regresion
    #
    
    axes[0,1].scatter(fittedValues,residuals,s = 5, color = 'gray')
    axes[0,1].set_ylabel('Residual', fontweight = 'bold')
    axes[0,1].set_xlabel('Fitted values', fontweight = 'bold')
    axes[0,1].axhline(y=0,color = 'k')
    prettyplot(axes[0,1])
    
    # (Subplot 3)
    # Q-Q plot. Analyze the distribution of residuals for departure from 
    # normality.
    #
   
    pp = sm.ProbPlot(residuals,stats.t, fit=True)
    qq = pp.qqplot(marker='.', markerfacecolor='gray', markeredgecolor='gray',
                   alpha=0.5,ax=axes[1,0])
    sm.qqline(axes[1,0], line='45', fmt='k-')
    
    axes[1,0].set_title('Normal Q-Q Plot')
    axes[1,0].set_xlabel('Theoretical quantiles',fontweight = 'bold')
    axes[1,0].set_ylabel('Sample quantiles',fontweight = 'bold')
    prettyplot(axes[1,0])
    
    # (Subplot 4)
    # Look at residuals by year. See if any paterns or notable departures
    # Residuals can be thought of like the errors.A zero residual means perfect prediction. 
    # Some questions to ask: Was there a really bad year for the model? Are there
    # trends in the residuals over time (e.g. did the model perform badly for
    # recent years 
    #
    
    axes[1,1].plot(residuals,color = 'k')
    axes[1,1].axhline(y=0,color = 'k')
    
    axes[1,1].set_xlabel('Year',fontweight = 'bold')
    axes[1,1].set_ylabel('Residual',fontweight = 'bold')
    
    axes[1,1].set_xlim([residuals.index.min(),residuals.index.max()])
    
    prettyplot(axes[1,1])

    plt.subplots_adjust(top=0.97,left = 0.1,right=0.95,bottom=0.11,hspace= 0.45,
                        wspace=0.5)
    
    # Change the default dpi: dots per inch! This is high resolution stuff!!!
    # Larger dpi, larger size file...beware!
    #fig.savefig('./Fig_10.png',dpi = 500)
    
    
    # Overall assessment: decent model!  Not obvious violations of assumptions
        
        
        
        
    
       
   
