# -*- coding: utf-8 -*-
"""

PURPOSE: Same as batch_dssat_2.py but uses parallel processing on a multi-core
architecture. If your machine doesnt have multiple cores, do not run this.

Sends a subset of soil_ids to each core. 

    Wihtin each core, this file does:
        
        (1) Uses the soybean DSSAT model 
        (2) Uses a default control file for soybean experiments 
            Runs all treatments in the file
        (3) Uses default control file as template
            Inserts new soil from .SOL 
        (4) Runs DSSAT with the modified treatment file from the command line
        
        This script uses input file that are provided by DSSAT on initial
        download. 
        
        Each soil will have its own directory within the overall experiment
    

AUTHOR: Zachary Zambreski, Kansas State University (2020)

Created on Tues Dec 21 8:30:10 2020

"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import subprocess
import os
import multiprocessing as mp
import time
import numpy as np

#------------------------#
# USER-DEFINED FUNCTIONS #
#------------------------#

def chunks(l, n):
    
    """ Yield successive n-sized chunks from l."""
    
    for i in range(0, len(l), n):
        yield l[i:i + n]

def cpuProcess(package):
    
    """  Function that the core uses to run DSSAT for limited # of soil IDs.
    
        Core cannot see global variables so we pass it all the path info defined
        in the inputs. 
    
    """
  
    # Unpack the data based directly to the core
    soils,expPath,dPath = package
    
    # Unpack the DSSAT related paths from "dpath"
    pathDSSAT, model, runmode = dPath
    
    # Unpack the experiment related paths from "epath"
    resultsDir,EXPNAME,controlFile,skeletonFile = expPath
    
    errorSoils = []
    
    # Iterate soils in .SOL
    for s,soil in enumerate(soils):
        
        # Create new output directories for the soil
        oDir = '%s/%s/%s'%(resultsDir,EXPNAME,soil)
        if not os.path.exists(oDir):
            print('Creating output directory')
            os.makedirs(oDir)
        
        # Use the skeleton file to write a new exp file to output folder using
        # a different soil class
        eFile  = controlFile       
        oFile  = open('%s/%s'%(oDir,eFile),'w')
        countI = -1000
        # Not super elegant but gets the job done
        with open(skeletonFile, 'r+') as f:
            
            lines = f.readlines()
            
            # Iterate each line in control file
            for i in range(0, len(lines)):
                
                line = lines[i]
                
                # Parse field section of control file
                if line[:7] == '*FIELDS':
                    countI   = i+2
                    fieldRow = lines[countI]
                    outField = fieldRow.replace(fieldRow[69:79],soil)     
                
                # Write new field
                if i != countI:
                    oFile.write(line)
                else:
                    oFile.write(outField) 
        
        # Close new control file
        oFile.close()
        
        #-------#
        # DSSAT #
        #-------#
        
        try:
        
            print('Running DSSAT for %s, %s, %d'%(soil,eFile,s))
            
            # Change directory to the location of experiment file
            os.chdir('%s'%(oDir))
            
            # Format the full command as a string
            command = "%s %s %s %s"%(pathDSSAT,model,runmode,eFile)
            
            # Pass the command to the system (Runs DSSAT for input options)
            subprocess.check_call(command, shell=True)
            
        except:
            
            errorSoils.append(soil)
      
    return errorSoils

#------#
# MAIN #
#------#

if __name__== "__main__":
    
    #--------#
    # INPUTS #
    #--------#
    
    # Location of DSSAT folder on your machine
    # I belive C:/ drive is default for windows OS
    tierDir = 'C:/DSSAT47'
    
    # Path to DSSAT executable
  
    pathDSSAT = '%s/DSCSM047.exe'%(tierDir)
    
    # DSSAT model (crop-specific)
    model = 'SBGRO045' # soybean, I think?
    
    # A: Run all treatments  (FileX)
    # B: Batch file name
    # E: Sensitivty analysis (FileX TN) .. TN is treatment number
    # N: Seasonal analysis   (bathfilename)
    # Q: Sequence analysis   (batchfilename)
    runmode   = 'A' 

    # Path to store your results
    resultsDir = '%s/Results'%(tierDir)
    # The overall experiment title
    EXPNAME    = 'Exp_Soils_Georgia_Seasonal_Parallel'
    
    # Path to .SOL table [used to extract soil IDs]
    path2sol = '%s/Soil/soil.sol'%(tierDir)
    
    # This control file will be used as the base for modifying additional experiments
    # In this script, we are just changing the soil id under the field section
    controlFile  = 'UFGA7812.SNX'
    # Path to control file
    skeletonFile = '%s/Seasonal/%s'%(tierDir,controlFile)
    
    #
    # Parallel processing 
    #
    
    # Number of computer cores to use
    nCores = 4
    
#%%############################################################################

    #-------------------------#
    # Get all soils from .SOL #
    #-------------------------#
    
    # Iterate the .SOL file and extract all IDs
    soilIDs = []
    inSoil  = open(path2sol,'r')
    for line in inSoil.readlines()[1:]: # Skip first line
        if line[0] == '*':
            soilIDs.append(line[1:11])
    inSoil.close()
    
    print('%d soils to perform experiments'%(len(soilIDs)))

#%%---------------------------------------------------------------------------#

    #------------------------#
    # Parallel process DSSAT #
    #------------------------#
    
    # Count number of cores on your machine
    # Many home machines are quad-core these days  (4)
    # (hypethreading doubles "logical cores" to 8)
    maxCores = mp.cpu_count()
    
    # Don't use more than you have
    if maxCores < nCores:
        nCores = maxCores - 1
    
    print('')
    print('Your computer has %d cores (includes hyperthreading)'%(maxCores))
    print('You selected %d cores'%(nCores))
    input("Press Enter to continue...") 
    
    # Divide the soil_ids list into nCore processings
    splits = list(chunks(soilIDs,int(len(soilIDs)/nCores)))
    
    # Add information to each split that needs to be passed
    # The core can't see anything in the inputs section
    dPathInfo = [pathDSSAT,model,runmode]
    expPath   = [resultsDir,EXPNAME,controlFile,skeletonFile]
    subsets   = [[soils,expPath,dPathInfo] for i,soils in enumerate(splits)]
    
    # Create the pool of processes (pool)
    # Pass the function and data splits to each core
    pool     = mp.Pool(processes = len(subsets))       
    tic      = time.time()
    results  = pool.map(cpuProcess,subsets)
    pool.close()
    toc      = time.time()
    print('Parallel processing time: %.2f minutes' %((toc - tic)/60))
    nWorkers = np.shape(results)[0]  
    
    input("Press Enter to continue...") 

#%%---------------------------------------------------------------------------#
    #--------------------#
    # Output information #
    #--------------------#
    
# =============================================================================
#     print('************')
#     print('%d soils failed simulation'%(len(errorSoils)))            
#     [print('%s failed'%(s)) for s in errorSoils]
# =============================================================================
