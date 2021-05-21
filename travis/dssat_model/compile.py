# -*- coding: utf-8 -*-
"""

PURPOSE: Run commands to compile DSSAT on windows. This script avoids having
to manually type them each time we make changes to the Fortran code. 

    This needs to be run from the command line in your Cygwin shell. For example, 
    in Cygwin navigate to the directory with this file and type:
        "python compile.py"

AUTHOR: Zachary Zambreski, Kansas State University (2021)

Created on Mon Apr 26 13:50:47 2021

"""

#--------------------#
# LIBRARIES IMPORTED #
#--------------------#

import os


#------#
# MAIN #
#------#

if __name__== "__main__":
    
    #--------#
    # INPUTS #
    #--------#
    
    # Upper-level Directory where DSSAT is stored
    TIERDIR  = "./model_1/dssat-csm-os"
    # PATH to LINK.TXT file
    LINKPATH = '%s/Build/CMakeFiles/dscsm047.dir/'%(TIERDIR)
    
    # Set True if want to build from scratch. Really only necessary if you 
    # REALLY MESS Something Up
    FULLCLEAN = False

#%%--------------------------------------------------------------------------#
   
    # Change working directory
    os.chdir(TIERDIR)
    
    if FULLCLEAN:
        """ Clean any builds; start from scratch """
        try:
            os.system('cmake -P distclean.cmake')
            # Remove the current executable file
            os.system('rm dscsm047.exe')
        except:
            pass
        
        os.system('mkdir ./build')
        os.chdir('build')
        os.system('cmake .. -DCMAKE_BUILD_TYPE=RELEASE')
        
        # Edit the link.txt file to remove the paths
        FLAGSDEL = ["-static", "-static-libgcc" "-static-libgfortran"]
        INFILE_ITEMS = open(LINKPATH + 'link.txt','r').readlines()[0].split(' ')
        s = ''
        for item in  INFILE_ITEMS:
            if item not in FLAGSDEL:
                s = s + item + ' '
        OFILE = open(LINKPATH + 'link.txt','w')
        OFILE.write(s)
        OFILE.close()
        
    else:
        
        ''' Recompile the scripts that were updated and created new exe '''      
        os.chdir('./build/')
        
        # Recompile any new files
        os.system('make')
    
    os.system('mv ./bin/dscsm047.exe ..')
    os.chdir('../')
    os.system('./dscsm047.exe A UFGA7801.SBX')
   
    