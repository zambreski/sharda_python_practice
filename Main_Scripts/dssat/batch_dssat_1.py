# -*- coding: utf-8 -*-
"""

PURPOSE: Run DSSAT experiments from command line. Run treatments for all soils
in a .SOL file. This script is illustrating for .SBX file

    This particular file does:
        
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

Created on Mon Dec 21 09:45:10 2020

"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import subprocess
import os

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
    EXPNAME    = 'Exp_Soils_Georgia'
    
    # Path to .SOL table [used to extract soil IDs]
    path2sol = '%s/Soil/soil.sol'%(tierDir)
    
    # This control file will be used as the base for modifying additional
    # experiments. In this script, we are just changing the soil id under the 
    # field section.
    controlFile  = 'UFGA7801.SBX'
    # Path to control file
    skeletetonFile = '%s/Soybean/%s'%(tierDir,controlFile)
    
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
    #---------------------------------#
    # Prepare and run the experiments #
    #---------------------------------#
    
    # List to store which soils fail in DSSAT simulation
    errorSoils = []

    # Iterate soils in .SOL
    for s,soil in enumerate(soilIDs):
        
        # Create new output directories for the soil
        oDir = '%s/%s/exp_%d_%s'%(resultsDir,EXPNAME,s,soil)
        if not os.path.exists(oDir):
            print('Creating output directory')
            os.makedirs(oDir)
        
        # Use the skeleton file to write a new exp file to output folder using
        # a different soil class
        eFile  = controlFile       
        oFile  = open('%s/%s'%(oDir,eFile),'w')
        countI = -1000
        # Not super elegant but gets the job done
        with open(skeletetonFile, 'r+') as f:
            
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

#%%---------------------------------------------------------------------------#
    #--------------------#
    # Output information #
    #--------------------#
    
    print('************')
    print('%d soils failed simulation'%(len(errorSoils)))            
    [print('%s failed'%(s)) for s in errorSoils]