# clean data scraped from city_meetings scrapy spider 

import pandas as pd
import datetime as dt


# import csv file 
data = pd.read_csv('city_meetings_raw.csv', skipinitialspace = True, index_col=False)


# remove unicode chars from Addresses
# remove double spaces
# convert 'Date' column  to pandas datetime object
data.Location.replace({r'[^\x00-\x7F]+':' '}, regex=True, inplace=True)
data.Location.replace({r'  ':' '}, regex=True, inplace=True)
data['Date'] = pd.to_datetime(data['Date'])


# sort data by date and set 'date' column as index
data = data.sort_values(by='Date')
data.set_index('Date', inplace=True)

# add index column
data =  data.reset_index(drop=False)

# export to csv file 
data.to_csv("city_meetings_clean.csv", index=False)

