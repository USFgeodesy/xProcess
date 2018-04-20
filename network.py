"""
Class for holding newtork of GPS sites

Nick Voss USF Geodesy

borrowed heavily from obspys catalog
"""

import glob
import io
import copy
import os
import warnings

import numpy as np
import pandas as pd
from station import Station


class Network(object):
    """
    Holds a collection of GPS stations as well as metadata on the Network
    with a few useful functions
    """
    def __init__(self, stations=None, **kwargs):
        if not stations:
            self.stations = []
        else:
            self.stations = stations



    def addStations(self,stationList):
        '''
        read a text file containtining:
        Station Lon Lat Height
        add to stations
        '''
        df = pd.read_fwf(stationList,names=['name','Lon','Lat','Height'])
        stations = []
        for i,name in enumerate(df.name):
            stations.append(Station(name,df.Lat[i],df.Lon[i],df.Height[i],data = '/home/nvoss/rnx/CR/CGPS/CR2/CGPS/CGPS/%s/*/*'%(name)))
        self.stations = stations
    def process(self):
        for station in self.stations:
            #make a directory to store processed station
            os.system('mkdir %s_pr'%(station.name))
            #change to the directory
            os.chdir('%s_pr'%(station.name))
            #copy the tree overview
            os.system('cp -r ../Trees .')
            #process the station
            station.process(tree='Trees')
            # go back a directory
            os.chdir('..')
