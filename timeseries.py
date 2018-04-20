'''
Class for holding a GPS time series
'''
import pandas as pd

class TimeSeries(object):
    '''
    time series object
    '''
    def __init__(self):
        self.dataframe = pd.DataFrame(columns=['Time','X','Y','Z','UX','UY','UZ'])

    def add_data(self,df):
        self.dataframe = self.dataframe.append(df,ignore_index=True)
    def save(self,station):
        self.dataframe.to_csv('station'+'.csv')
