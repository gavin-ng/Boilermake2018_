# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 00:25:12 2018

@author: Gavin
"""
#import json
#import urllib2
import datetime
import pandas as pd
import copy


##############
## GET DATA ##
##############
#
###open url
#url =  "https://data.urbanaillinois.us/resource/t48r-g9bk.json?$$app_token=CgIgMgqsvbPxqB29l12Rm32Dp"
#data = json.load(urllib2.urlopen(url))
#df = pd.DataFrame(data)


df = pd.read_csv("C:\Users\Gavin\Documents\Police_Incidents_Since_1988.csv")


# get today's date and format to match data
# convert to months

today = datetime.date.today().strftime("%Y%m%d")
#today = int(str(int(today[0:4] + today[4:6])))
today = (int(today[0:4]) * 12) + int(today[4:6])

################
## CLEAN DATA ##
################


# replace spaces in column headers with underscores
df.columns = [c.replace(' ', '_') for c in df.columns]


# clean up the date format
# this returns YYYYMM (no DAY info in data)
def clean_date(date_str):
    return int(str(date_str)[6:])*12 + int(str(date_str)[0:2])

df['DATE_IN_MONTHS'] = df['DATE_OCCURRED'].apply(clean_date)


# get co-ordinates
# co-ordinates are marked by (lat, long) 
# i.e. wrapped in parentheses with a comma in between
def get_coord(address_str):
    try:
        gps = address_str[address_str.find("(") +1: address_str.find(")")]

#        gps = gps.replace("," , "")
        return gps
    except AttributeError:
        return None
    
def get_lat(gps):
    try:
        lat = gps[gps.find("(") +1: gps.find(",")]
        return float(lat)
    except AttributeError:
        return None
    
def get_lng(gps):
    try:
        lng = gps[gps.find(",") +2: gps.find(")")]
        return float(lng)
    except AttributeError:
        return None
    


df['GPS'] = df['MAPPING_ADDRESS'].apply(get_coord)



#### Make a clean dataframe ####

clean_df = copy.copy(df)
# drop NAs and select rows with coordinates
clean_df = clean_df.dropna(subset=['GPS'])
clean_df = clean_df[clean_df.GPS.str.contains("\n", na=False) == False]

clean_df['LAT'] = clean_df['GPS'].apply(get_lat)
clean_df['LNG'] = clean_df['GPS'].apply(get_lng)


# some rows have missing/improper dates. remove those
# dataset is supposed to be from 1988 onwards
# that would be 23856 monhts
clean_df = clean_df[clean_df.DATE_IN_MONTHS > 23856 ]

# calculate the number of months from the current month. used to make weights
clean_df['DATE_DIFF'] = clean_df.DATE_IN_MONTHS.apply(lambda x: today - x)

# weight the data according to number of months from the current month
# weights decrease exponentially as a function of time
clean_df['WEIGHT'] = clean_df.DATE_DIFF.apply(lambda x: 1.0/(x+1))

# make a dataframe with columns that we want
cols = ['DATE_DIFF', 'WEIGHT', 'LAT', 'LNG', 'CRIME_CATEGORY', 'CRIME_CATEGORY_DESCRIPTION']

final_df = clean_df[cols]