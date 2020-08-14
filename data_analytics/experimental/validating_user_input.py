import pandas as pd
import csv
import time
import datetime
import numpy as np
import os
from datetime import datetime
from time import gmtime
from time import strftime


calendar_dates = pd.read_csv('~/Desktop/google_transit_dublinbus/calendar_dates.txt')
routes = pd.read_csv('~/Desktop/google_transit_dublinbus/routes.txt')
calendar = pd.read_csv('~/Desktop/google_transit_dublinbus/calendar.txt')
stop_times = pd.read_csv('~/Desktop/google_transit_dublinbus/stop_times.txt')
trips = pd.read_csv('~/Desktop/google_transit_dublinbus/trips.txt')


route = '44'
direction = 1 
start_stop = 207
end_stop = 2825
date = "2020-07-23"
time = 10000

def get_weekday(date):
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')
    day_of_week =  datetime.date(date_time_obj).weekday()
    return day_of_week


def get_name_day_of_week(day_of_week):
    days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    name_day_of_week = days[day_of_week]
    return name_day_of_week


def get_integer_date(date):
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')
    timestampStr = date_time_obj.strftime("%Y%m%d")
    date_int = int(timestampStr)
    return date_int


def is_exception(num):
    for index, row in calendar_dates['date'].items():
        if row == num:
            return calendar_dates['exception_type'].iloc[index]
        else:
            return 0


def get_service_id(date, name_day_of_week, exception_code):
    #poss_rows = []
    if exception_code == 0:
        for index, row in calendar['start_date'].items():
            if date >= row:
                if date <= calendar['end_date'].iloc[index]:
                    if calendar[name_day_of_week.lower()].iloc[index] == 1:
                        service_id = calendar['service_id'].iloc[index]

    else: 
        service_id = exception_code
    return service_id


def get_service_id(date, name_day_of_week, exception_code):
    #poss_rows = []
    if exception_code == 0:
        for index, row in calendar['start_date'].items():
            if date >= row:
                if date <= calendar['end_date'].iloc[index]:
                    if calendar[name_day_of_week.lower()].iloc[index] == 1:
                        service_id = calendar['service_id'].iloc[index]

    else: 
        service_id = exception_code
    return service_id

def get_range(time_range):
    departure_time = []
    for i in time_range:
        string_time = strftime("%H:%M:%S", gmtime(i))
        time_object_time = datetime.strptime(string_time,'%H:%M:%S')
        departure_time.append(time_object_time.time())
    
    return departure_time

def get_route_id(route):
    route_ids = []
    for index, row in routes['route_short_name'].items():
        if route.lower() == row:
            route_ids.append(routes['route_id'].iloc[index])
    return route_ids


def get_trip_ids(service_id, route_id, direction):
    route_ids_dataframe = (trips[trips['route_id'].isin(route_id)])
    service_id_dataframe = route_ids_dataframe[route_ids_dataframe['service_id'] == service_id]
    direction_id_dataframe = service_id_dataframe[service_id_dataframe['direction_id'] == direction-1]
    trip_ids = list(direction_id_dataframe['trip_id'])
    return trip_ids



def stop_formatter(stop):
    if len(str(stop)) == 0 or len(str(stop)) > 4:
        return "Error"
    elif len(str(stop)) == 1:
        stop_id = '8220DB00000' + str(stop)
    elif len(str(stop)) == 2:
        stop_id = '8220DB0000' + str(stop)
    elif len(str(stop)) == 3:
        stop_id = '8220DB000' + str(stop)
    elif len(str(stop)) == 4:
        stop_id = '8220DB00' + str(stop)
    return stop_id


def get_bus_times(trip_ids, first_stop, departure_time):
    stops_trips_dataframe = stop_times[stop_times['trip_id'].isin(trip_ids)]
    first_stop = stops_trips_dataframe[stops_trips_dataframe['stop_id'] == first_stop]
    bus_dept_times = []
    for index, row in first_stop['arrival_time'].items():
        bus_dept_time = datetime.strptime(row,'%H:%M:%S').time()
        if bus_dept_time >= departure_time[0] and bus_dept_time <= departure_time[1]:
            bus_dept_times.append(bus_dept_time)
    return(bus_dept_times)

day_of_week = get_weekday(date)
name_day_of_week = get_name_day_of_week(day_of_week)
date_int = get_integer_date(date)

# first query to db... look in calendar_dates to see if the date in question is there...
exception_code = is_exception(date_int)

# second query to db ... if it isn't ... use the date to get the service_id from calendar
service_id = get_service_id(date_int, name_day_of_week, exception_code)

time_range = [time, time+3600]
departure_time = get_range(time_range)

# third query to db ... get the big route_id from routes using the short route-id from user
route_id = get_route_id(route)

# fourth query to db ... get the trip_ids from trips using serice_id, direction and route_id
trip_ids = get_trip_ids(service_id, route_id, direction)

# I think this will be replaced by simple searching for the old stop no (eg. 226) at the end of the new stop number (eg 8220DB000226) ...
first_stop = stop_formatter(start_stop)
last_stop = stop_formatter(end_stop)

#fifth query to db ... in stop_times: use the trip_ids, the first stop number and the time ranges to get possible options
possible_buses = get_bus_times(trip_ids, first_stop, departure_time)

if len(possible_buses) > 0:
    print ("you may proceed", possible_buses)

else:
    print("Nope, one does not simply walk into Mordor!")
