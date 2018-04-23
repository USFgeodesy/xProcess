"""
Class for holding newtork of GPS sites

Nick Voss USF Geodesy

borrowed heavily from obspys station
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
from future.builtins import *  # NOQA
from future.utils import native_str

import glob
import pandas as pd
import subprocess
import logging
import io
import copy
import os
import warnings
import fileinput
import re
import sys
import numpy as np
from timeseries import TimeSeries

ionfile = '/home/nvoss/goa-var/cddis.gsfc.nasa.gov/gps/products/ionex'

class Station(object):
    """
    From the StationXML definition:
        This type represents a Station epoch. It is common to only have a
        single station epoch with the station's creation and termination dates
        as the epoch start and end dates.
    """
    def __init__(self,name,latitude, longitude, elevation, data=None,
                 monument=None,setting=None, antenna=None,jump_list=None,
                 operators=None):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.elevation = elevation
        self.data = data or []
        self.monument = monument
        self.setting = setting
        self.operators = operators or []

    def plot_map(self):
        '''
        plot a map of the station
        '''
        return
    def process(self,tree=None,start_date=None,end_date=None):
        '''
        Process each day between start date and end date if it exists.
        tree is a tree object
        '''
        import glob
        import pandas as pd
        import fileinput
        import subprocess

        global ionfile
        print('Process %s'%(self.name))
        logging.basicConfig(filename='xProcess.log',level=logging.DEBUG)
        #get all files in directory *data*
        files = glob.glob(self.data)
        print('Number of Found FIles :',len(files))
        logging.info('Rinex Files to be processed:\n')
	[logging.info(str(f)+'\n') for f in files]
	dt=0
        for f in files:
            #figure out what day it is
            #? read the rinex file check if day is already in TS?
            #process each day
            logging.info('Starting '+f)
            year = f.split('/')[-1][9:11]
	    if int(year)<50:
                year = str(int(year)+2000)
            else:
                year = str(int(year)+1900)
            day = f.split('/')[-1][4:7]
            logging.warning('Working on %s %s'%(day,year))
            ionFile = (ionfile+'/%s/%s/jplg%s0.%si'%(year,day,day,year[2:]))
            logging.debug('The ionex file is : %s'%(ionFile))
            date = subprocess.check_output('doy2date %s %s'%(day,year),shell=True)
            if f==files[0]:
                startDate = date #this is for netSeries, it is the reference day
            start = subprocess.check_output('date2sec %s 00:00:00'%(date[0:10]),shell=True)[0:11]
            end = subprocess.check_output('date2sec %s 23:59:59'%(date[0:10]),shell=True)[0:11]
            #make sure it hasn't been processed already
            if int(year)+int(day)/365.25>start_date and int(year)+int(day)/365.25<end_date:
                if not os.path.exists('%s.gdcov'%(date[:-1])):
                    #replace the flags in the trees
                    replace('Trees/Nick_0.tree',"GLOBAL_EPOCH ==",'GLOBAL_EPOCH == %s'%(start))
                    replace('Trees/Nick_0.tree',"IONEXFILE ==",'IONEXFILE == %s'%(ionFile))
                    #process
                    if tree is None:
                        os.system('gd2e.py -runType=PPP -rnxFile %s -gdCov -nProcessors=4 -GNSSproducts /home/nvoss/orbits/sideshow.jpl.nasa.gov/pub/JPL_GPS_Products/Final'%(f))
                    else:
                        os.system('gd2e.py -runType=PPP -treeS Trees -rnxFile %s -nProcessors=4 -gdCov -GNSSproducts /home/nvoss/orbits/sideshow.jpl.nasa.gov/pub/JPL_GPS_Products/Final'%(f))
                    os.system('cp smoothFinal.gdcov %s.gdcov'%(date[:-1]))
                    os.system('mkdir %s_ran%s'%(self.name,year))
                    os.system('mkdir %s_ran%s/%s'%(self.name,year,day))
                    os.system('cp runAgain %s_ran%s/%s'%(self.name,year,day))
                    os.system('cp *.tree.err0_0 %s_ran%s/%s'%(self.name,year,day))
                    os.system('cp *.tree.log0_0 %s_ran%s/%s'%(self.name,year,day))
                    logging.debug('Saved tree and logs to file')
		    dt = date[:-1]
		    os.system('netSeries.py -r %s.gdcov -i *.gdcov'%(dt))
            else:
                logging.warning('File outside date range not processed')
        #if dt!=0:
	#	os.system('netSeries.py -r %s.gdcov -i *.gdcov'%(dt))

def splitline(line):
  index,sta,time,position,unc = line.split(' ')
  return int(time),float(position),float(unc)

def replace(fil,inp,output):
    for line in fileinput.input(fil,inplace=True):
        # Whatever is written to stdout or with print replaces
        # the current line
        if line.startswith(inp):
            print(output)
        else:
            sys.stdout.write(line)
