import pandas as pd
import csv
import numpy as np
import datetime
from time import gmtime
from time import strftime
import sys
import warnings
warnings.filterwarnings('ignore')

def process_leave_times(route_file, leavetime_file, mode):
	#read in files
	leavetimes = pd.read_csv(leavetime_file, keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
	route = pd.read_csv(route_file, keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)


	only_route = pd.merge(leavetimes,
                 route[[',DATASOURCE', 'TRIPID', 'DAYOFSERVICE', 'LINEID', 'ROUTEID', 'DIRECTION']],
                 on=['TRIPID', 'DAYOFSERVICE'])


	#setting types
	only_route['DAYOFSERVICE'] = only_route['DAYOFSERVICE'].astype('datetime64[ns]')
	only_route['TRIPID'] = only_route['TRIPID'].astype('category')
	only_route['PROGRNUMBER'] = only_route['PROGRNUMBER'].astype('category')
	only_route['STOPPOINTID'] = only_route['STOPPOINTID'].astype('category')
	only_route['LINEID'] = only_route['LINEID'].astype('category')
	only_route['DIRECTION'] = only_route['DIRECTION'].astype('category')
	only_route['ROUTEID'] = only_route['ROUTEID'].astype('category')
    
    #Renaming and curtailing 'DATASOURCE
	unique_trips = list(only_route[',DATASOURCE'])
	unique_trips_new = []
	for i in unique_trips:
		j = i[0:-4]
		unique_trips_new.append(j)
	
	only_route['UNIQUE_TRIP'] = unique_trips_new
	del only_route[',DATASOURCE']
    

	#Creating Month Feature
	only_route['MONTH'] = only_route['DAYOFSERVICE'].dt.month

	#Creating Day of week Feature
	only_route['DAYOFWEEK'] = only_route['DAYOFSERVICE'].dt.dayofweek

	#Creating arrival time Feature
	arrival_time = []

	for row in only_route['ACTUALTIME_ARR']:
    		x = strftime("%H:%M:%S", gmtime(row))
    		arrival_time.append(x)

	only_route['ARRIVALTIME'] = arrival_time
            
	#Creating departure time Feature
	departure_time = []

	for row in only_route['ACTUALTIME_DEP']:
    		x = strftime("%H:%M:%S", gmtime(row))
    		departure_time.append(x)

	only_route['DEPARTURETIME'] = departure_time

	#Creating Feature Delay Arrival
	only_route['DELAYARR'] = only_route['PLANNEDTIME_ARR'] - only_route['ACTUALTIME_ARR']

	#Creating Feature Delay Departure
	only_route['DELAYDEP'] = only_route['PLANNEDTIME_DEP'] - only_route['ACTUALTIME_DEP']

	#Creating dwell Time Feature
	only_route['DWELLTIME'] = only_route['ACTUALTIME_DEP'] - only_route['ACTUALTIME_ARR']

	#Creating Time Group Feature
	time_group_departure = []
	for row in only_route['ACTUALTIME_DEP']:
        	if row < 0: 
           		 print ("Error - negative time stamp")
        
        	elif row <= 3600 or (row > 86400 and row <= 90000):
            		time_group_departure.append('0')
        	elif row > 3600 and row <= 7200 or (row > 90000 and row <= 93600) :
            		time_group_departure.append('1')
        	elif row > 7200 and row <= 10800:
            		time_group_departure.append('2')
        	elif row >10800 and row <= 14400:
            		time_group_departure.append('3')
        	elif row > 14400 and row <= 18000:
            		time_group_departure.append('4')
            
        	elif row > 18000 and row <= 21600:
            		time_group_departure.append('5')
        	elif row > 21600 and row <=25200:
            		time_group_departure.append('6')
        	elif row > 25200 and row <= 27000:
            		time_group_departure.append('7')
        	elif row > 27000 and row <= 28800:
            		time_group_departure.append('8')
        	elif row > 28800 and row <= 30600:
            		time_group_departure.append('9')
            
        	elif row > 30600 and row <= 32400:
            		time_group_departure.append('10')
        	elif row > 32400 and row <= 36000:
            		time_group_departure.append('11')
        	elif row > 36000 and row <= 39600:
            		time_group_departure.append('12')
        	elif row > 39600 and row <= 43200:
            		time_group_departure.append('13')
        	elif row > 43200 and row <= 46800:
            		time_group_departure.append('14')
            
        	elif row > 46800 and row <= 50400:
            		time_group_departure.append('15')
        	elif row > 50400 and row <= 54000:
            		time_group_departure.append('16')    
        	elif row > 54000 and row <= 57600:
            		time_group_departure.append('17')
        	elif row > 57600 and row <= 59400:
            		time_group_departure.append('18')
        	elif row > 59400 and row <= 61200:
            		time_group_departure.append('19')
        
        	elif row > 61200 and row <= 63000:
            		time_group_departure.append('20')
        	elif row > 63000 and row <= 64800:
            		time_group_departure.append('21')
        	elif row > 64800 and row <= 66600:
            		time_group_departure.append('22')
        	elif row > 66600 and row <= 68400:
            		time_group_departure.append('23')
        	elif row > 68400 and row <= 72000:
            		time_group_departure.append('24')
        
        	elif row > 72000 and row <= 75600:
            		time_group_departure.append('25')
	        elif row > 75600 and row <= 79200:
        	    	time_group_departure.append('26')
	        elif row > 79200 and row <= 82800:
            	        time_group_departure.append('27')
        	elif row > 82800 and row <= 86400:
            	    	time_group_departure.append('28')


	only_route['TIME_GROUP'] = time_group_departure
    
    
    
    #get dynamic name for saving .csv files
	x = str(route_file)
	y = x[0:-4]
	filename = y +"_Master.csv"
    
	#Write/Append to route master file.
	if mode == 'initial':
		only_route.to_csv(filename, index=False)

	else:
		only_route.to_csv(filename, mode='a', header=False, index=False)

if __name__ == "__main__":
	a = sys.argv[1]
	b = sys.argv[2]
	c = sys.argv[3]

	process_leave_times(a,b,c)
