# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 23:00:12 2018

@author: Gavin
"""

import json
import urllib2
import pandas as pd   
import datetime
import numpy as np

map_url = "https://route.api.here.com/routing/7.2/calculateroute.json?waypoint0=40.4237054%2C-86.92119459999998&waypoint1=40.10195230000001%2C-88.22716149999997&mode=fastest%3Bpedestrian&alternatives=4&representation=display&app_id=devportal-demo-20180625&app_code=9v2BkviRwi9Ot26kp2IysQ"
map_data = json.load(urllib2.urlopen(map_url))    

crime_url = "https://data.cityofchicago.org/resource/crimes.json?$limit=10"
crime_data_raw = json.load(urllib2.urlopen(crime_url))


## Clean data

today = int(datetime.date.today().strftime("%Y%m%d"))

# remove NaNs and nas
crime_data = pd.DataFrame(crime_data_raw)
crime_data = crime_data.replace(np.NaN, np.nan).dropna(axis=0)


# clean up the date format
# this returns YYYYMM (no DAY info in data)
def date_diff(date_str):
    clean_date = int((str(date_str)[:10]).replace("-",""))
    diff = today - clean_date
    return (diff)


# weight the data according to number of months from the current month
# weights decrease exponentially as a function of time
    
crime_data['date_diff'] = crime_data['date'].apply(date_diff)
crime_data['date_weight'] = crime_data.date_diff.apply(lambda x: 1.0/(x+1.0))

cols = ["fbi_code", "latitude", "longitude", "primary_type", "date_weight", "date"]

crime_df = crime_data[cols]



### DONE WITH CLEANING


#### Get routes

coords = [i['shape'] for i in map_data['response']['route']]


zzz = [i['shape'] for i in map_data['response']['route']]
    
#def get_total_weights(array, data):
#    total_weights = 0
#    for index in range(len(array) - 1):
#        lat1 = min(float(array[index][0]), float(array[index+1][0]))
#        lat2 = max(float(array[index][0]), float(array[index+1][0]))
#    
#        lng1 = max(float(array[index][1]), float(array[index+1][1]))
#        lng2 = min(float(array[index][1]), float(array[index+1][1]))
#    
#        coord_data = data[(data.LAT >= lat1) & (data.LAT <= lat2) & (data.LNG <= lng1) & (data.LAT >= lng2)]
#        total_weights += coord_data.WEIGHT.sum()
#    return total_weights


    
def get_total_weights(coord_array, crime_data):
   
    total_weights = 0
    # for each route
    for i in range(len(coord_array)):
        # for each coordinate
        for j in range(len(coord_array[i])):
            xy = coord_array[i][j].split(",")
            
            # for each coordinate, get all crimes within radius
            x1 = np.repeat(float(xy[0]), len(crime_df))
            y1 = np.repeat(float(xy[1]), len(crime_df))
            
#            x1 = np.asarray(crime_df['longitude'])
            x2 = crime_df['longitude'].apply(lambda x: float(x))
            y2 = crime_df['latitude'].apply(lambda x: float(x))
            
            # r is a list of distances (Euclidean) of crimes from this coordinate
            r = (x1 - x2)**2 + (y1 - y2)**2
            
            
#            

        
        
        
    return (r)
            
            

        
        
a = get_total_weights(zzz, crime_df)
