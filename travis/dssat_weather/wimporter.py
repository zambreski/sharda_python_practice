'''
Script to import future climate data into DSSAT 4.7

@author: Garvey Engulu B. Smith <garveyebsmith@live.com>
@author: Zaichen Xiang <xzckay198763@gmail.com>
@author: Allan Andales <Allan.Andales@colostate.edu>
@date: 11/08/2019
@website: http://ogallalawater.org/

@ Zach Zambreski modified this script April 2021

# ! Notes: 
# ! i.  The configuration file (configuration.xlsx) needs to be filled.
# ! ii. The script will currently work for a maximum of 99 gcms in a directory/ 
# !     sub-directory.
# !     
# Change log
v1.0
# Working script
# script reads in weather files and co2 concentrations using parameters set in the configuration.
# TODO:
    - possibly dispaly configuration option at the start of script.
v0.9.0
    - Working basically (able to import files and write weather files)
# TODO: 
    - write out info on station, path, and weather station
'''

import collections
import numpy as np
import pandas as pd
from pathlib import Path
import sys

CURRENT_DIRECTORY = Path(sys.argv[0]).parent
FILE_CONFIGURATION_1 = 'config_1_weather_importer.xlsx'
# FILE_CONFIGURATION_1 = sys.argv[1]
LATEST_YEAR = 2100
# RUN_SCRIPT = True    

# credits
HEADER_TEXT = (
    '######################################################################'
    '######\n'
    '\n'
    'GCM WEATHER IMPORTER FOR DSSAT\n'
    'authors: Garvey E. B. Smith <garvey.smith@colostate.edu>\n'
    '         Zaichen Xiang <xzckay198763@gmail.com>\n'
    '         Allan Andales <Allan.Andales@colostate.edu>\n'
    'website: http://ogallalawater.org/\n'
    'Date:    Jan-24-2020\n'
    '\n'
     'MODIFIED BY ZACH ZAMBRESKI 2021'
    '######################################################################'
    '#######\n'
)

print(HEADER_TEXT)
# 1. Import configuration
print(''.join([
    '# 1. Importing configuration\n',
    'configuration file: ',
    FILE_CONFIGURATION_1
    ]),
    end = '\n\n'
)

try:
    df_config = pd.read_excel(FILE_CONFIGURATION_1,
                    sheet_name='config_1', skiprows=2, index_col=0,
                    usecols=[0, 1], header=1)
    
    # configuration parameters
    TARGET_DIRECTORY = str(df_config.at['target_directory', 'Value'])
    OUT_DIRECTORY = Path(str(df_config.at['out_directory', 'Value']))
    STATION_PREFIX = str(df_config.at['station_prefix','Value'])[:2].upper()
    LATITUDE = float(df_config.at['latitude', 'Value'])
    LONGITUDE = float(df_config.at['longitude', 'Value'])
    ELEVATION = int(df_config.at['elevation', 'Value'])
    INSTRUMENT_HEIGHT = float(
        df_config.at['instrument_height', 'Value'])
    ANEMOMETER_HEIGHT = float(
        df_config.at['anemometer_height', 'Value'])
    FILE_LEGEND_GCMS_DSSAT_STATIONS = 'gcm-dssat_station_legend.csv'
    
except Exception as e:
    print(e, '\nFailed to import configuration!', end='\n')
    input("Enter any key to quit.")

def main():
    '''
    Main script
    '''

    # 2. search target director for gcm weather files
    print(''.join([
        '# 2. Searching for weather series to import\n',
        'directory: ',
        TARGET_DIRECTORY
        ]),
        end = '\n\n'
    ) 
    while(True):
        try:
            dssat_weather_stations = []  # names for dssat weather stations
            wfiles_in = {}      # dictionary for gcm file name, path, and dssat
            
            # weather station name
            # file_list = []      # file paths
            filenames = []     # file names
            station_counter = 1
  
            for file in Path(TARGET_DIRECTORY).rglob('*.[Cc][Ss][Vv]'):
                # Stop script if duplicate gcm file names found in target
                # directory
               
                filenames.append(str(file).split(
                    '\\')[-1])  # extract file name
                
                for filename in filenames:
                    if filenames.count(filename) > 1:
                        err_msg = ''.join(
                            ['Duplicate filenames found in target directory.',
                                '\nCheck: ', filename])
                        raise Exception(err_msg)
                dssat_station_name = '{}{:>02}'.format(STATION_PREFIX,
                                                        station_counter)
                # create dictionary: keys=gcm file name, values= file path,
                # station name
                wfiles_in[str(file).split('\\')[-1]] = [str(file),
                                                        dssat_station_name]
                dssat_weather_stations.append(dssat_station_name)
                station_counter += 1
            break

        except Exception as e:
            print(e, '\nError: Failed to import gcm weather files!', end='\n')
            input("Enter any key to quit.")
            break

    def read_weather_csv(file):
        '''
        reads gcm csv file into a pandas dataframe calculating annual 
        average temperature and the average of monthyly temperature 
        amplitudes monthly

        Parameters:
        file: str
            path to file
        Returns:
        ws: namedtuple
            df :    weather series pandas DataFrame 
            tmeans: list of annual temperature averages, 
            tamps:  list of the annual average of monthyly temperature 
                    amplitudes
        '''

        try:
            # import csv
            dfw = pd.read_csv(file, parse_dates=[0])
            # check for missing values in csv file
            if dfw.isna().any().any():
                err_msg = 'Error: Missing value in input file: ' + str(file)
                raise Exception(err_msg)

            else:
                # rename columns
                dfw.rename(columns={
                    'tasmax': 'tmax',
                    'tasmin': 'tmin',
                    'pr': 'prec',
                    'rsds': 'srad',
                }, inplace=True)

                dfw['tmean'] = dfw[['tmax', 'tmin']].mean(axis=1)
                dfw['year'] = pd.DatetimeIndex(dfw['Date']).year
                dfw['month'] = pd.DatetimeIndex(dfw['Date']).month
                dfw['day'] = pd.DatetimeIndex(dfw['Date']).day
                dfw['doy'] = pd.DatetimeIndex(dfw['Date']).dayofyear
                dfw['dewp'] = np.nan
                dfw['par'] = np.nan
                dfw['evap'] = np.nan
            
            # select all years below 2100 (DSSAT wth files use 2 digit years
            # in their time series. 2000 and 2100 will have the same 
            # date-doy value)
            dfw = dfw[dfw.year < LATEST_YEAR]
            # dfw['date_yydoy'] = dfw['date'].dt.strftime('%y') +\
            #                     dfw['doy'].astype(str)
            dfw['date_yydoy'] = dfw['year'].astype(str).str[-2:] +\
                dfw['doy'].astype(str).str.pad(width=3, fillchar='0')

            # annual tmean
            tmean_annual = dfw[['year', 'tmean']].\
                groupby(['year']).mean().to_dict('index')
            # convert dict to year: value
            tmean_annual = {
                k:v['tmean'] for k,v in tmean_annual.items()
            }  
            # annual tamp
            tmean_monthly = dfw[['year', 'month', 'tmean']].\
                groupby(['year', 'month']).mean()
            tmax_monthly_means = tmean_monthly.groupby(['year']).max()
            tmin_monthly_means = tmean_monthly.groupby(['year']).min()
            tamp_annual = (tmax_monthly_means - tmin_monthly_means).\
                to_dict('index')
            tamp_annual = {k:v['tmean'] for k,v in tamp_annual.items()}
            # wseries named tuple
            wseries = collections.namedtuple(
                'wseries', ['df', 'tmeans', 'tamps', 'file_path'])
            ws = wseries(df=dfw[['year', 'date_yydoy', 'srad', 'tmax',
                    'tmin', 'prec', 'dewp', 'wind', 'par', 'evap', 'rh','et'
                    ]].round({
                        'srad': 1, 'tmax': 1, 'tmin': 1, 'prec': 1,
                        'dewp': 1, 'wind': 1, 'par': 1, 'rh': 1,'et':1,
                    }),
                    tmeans=tmean_annual,
                    tamps=tamp_annual,
                    file_path=file)
            print('input file read: ', file)
            return ws

        except Exception as e:
            print(e, '\nError: Could not import csv file: ', file, end='\n')
            return None

    # 3. Read in gcm weather series and write DSSAT wth files
    while(True):
        # Check weather directory for old files and read new files
        try:
            # Get file paths for gcm weather files
            file_list = [file[0] for file in wfiles_in.values()]
            # Check if one or more files in the dssat weather folder have 
            # the same station prefix as in the configuration file
            print(''.join([
                '# 3. Checking if weather files with station prefix in ',
                'configuration already exist'
                ]), end = '\n'
            )
            wfile_list = Path(
               OUT_DIRECTORY).glob('*.[Ww][Tt][Hh]')
            station_prefixes = [str(value).split('\\')[-1][:2]
                                for value in wfile_list]
            check = [idx for idx in station_prefixes if idx.upper() ==
                    STATION_PREFIX]
            if(check):
                err_msg = ''.join(['Files found in \'', 
                                str(OUT_DIRECTORY),
                                '\' with the same station prefix, \'',
                                STATION_PREFIX, '\' as the configuration ',
                                'file.\nDelete these files ',
                                'and run script again.'
                ])
                raise Exception(err_msg)
            else:
                print(
                    'No previous dssat weather stations found!', 
                    end = '\n\n'
                )
                station_counter = 1
                weather_stations = {}
                future_weather_list = []

                # read in weather series and break their import in case 
                # there's an issue reading in one of the files
                print('# 4. Importing weather series', end = '\n')
                for file in file_list:
                    ws = read_weather_csv(file)
                    if(ws == None):
                        raise Exception()
                    else:
                        future_weather_list.append(ws)

                for wseries in future_weather_list:
                    
                    station_counter_fmt = '{:02}'.format(station_counter)
                    weather_station = ''.join(
                        [STATION_PREFIX, station_counter_fmt])
                    weather_stations[wseries.file_path] = weather_station
                    # get list of unique years to use in generating file names
                    wth_years = wseries.df.year.unique()
                    for year in wth_years:
                        yy = str(year)[-2:]
                        
                        # generate wth file name
                        wth_filename = ''.join(
                            [STATION_PREFIX, station_counter_fmt, yy, '01.WTH'])
                        
                        # create header
                        sect_header = ''.join(['*WEATHER DATA : {insi}\n',
                            '\n', '@ INSI      LAT     LONG  ELEV   TAV   AMP ',
                            'REFHT WNDHT    CO2\n',
                            '  {insi:>4} {lat:>8.3f} {long:>8.3f} {elev:>5} ',
                            '{tavg:>5.1f} {tamp:>5.1f} {ref_ht:>5.1f} ',
                            '{wind_ht:5.1f} {co2_conc:>6.1f}\n',
                            '@DATE  SRAD  TMAX  TMIN  RAIN  DEWP  WIND   PAR  ',
                            'EVAP  RHUM  PETO\n']).format(
                            insi=''.join(
                                [STATION_PREFIX, station_counter_fmt]),
                            lat=LATITUDE,
                            long=LONGITUDE,
                            elev=ELEVATION,
                            tavg=wseries.tmeans[year],
                            tamp=wseries.tamps[year],
                            ref_ht=INSTRUMENT_HEIGHT,
                            wind_ht=ANEMOMETER_HEIGHT,
                            co2_conc = -99.0)

                        # create values section               
                        sect_values = wseries.df[
                            wseries.df.year == year]\
                            .drop(columns='year').to_string(
                                header=False,
                                index=False,
                                formatters={
                                    'date_yydoy': '{:<5}'.format,
                                    'srad': '{:>5.1f}'.format,
                                    'tmax': '{:>5.1f}'.format,
                                    'tmin': '{:>5.1f}'.format,
                                    'prec': '{:>5.1f}'.format,
                                    'wind': '{:>5.1f}'.format,
                                    'rh': '{:>5.1f}'.format,
                                    'et':'{:>5.1f}'.format
                                },
                                na_rep='     ')
                        
                        

                        sect_values_n = ''
                        for line in sect_values.splitlines():
                            line = line[1:] +'\n'
                            sect_values_n += line 

                        # build full file
                        file_text = sect_header + sect_values_n
                        # write file
                        
                        wth_file =OUT_DIRECTORY.joinpath(
                            wth_filename)
                  
                        with open(wth_file, 'w') as f:
                            f.write(file_text)
                            print('wrote: ', wth_file, end='\n')

                    station_counter += 1

            # write gcm weather series - dssat weather station legend
            try:
                file_legend = CURRENT_DIRECTORY.joinpath(
                        FILE_LEGEND_GCMS_DSSAT_STATIONS
                )
                file_text = 'file,dssat_station_name,file_path\n'
                print(''.join([
                    '\n# 5. Writing legend of imported files\n',
                    'legend: ',
                    str(file_legend)
                    ]), 
                    end = '\n\n'
                )
                for k in weather_stations.keys():
                    file_text = file_text +\
                        '{},{},{}\n'.format(
                            str(k).split('\\')[-1],
                            weather_stations[k],
                            str(k)
                        )
                with open(file_legend, 'w') as f:
                    f.write(file_text)

                print(
                    ''.join([
                        '# 7. Script successfully completed\n',
                        'Find import summary in: ', 
                        str(file_legend),
                        '\nCopy this file to directory where the script to ',
                        'modify DSSAT 4.7 simulations will be run'
                    ]),
                    end = '\n'
                ) 

            except Exception as e:
                err_msg = ''.join(
                    ['Could not write station legend file: ',
                        str(file_legend)])
                print(e, err_msg, end='\n')
                input("Enter any key to quit.")
            break    
        except Exception as e:
            print(e, end='\n')
            input("Enter any key to quit.")
            break

if __name__ == "__main__":
    main()

