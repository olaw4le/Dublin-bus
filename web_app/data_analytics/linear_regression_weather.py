import pandas as pd
import pickle
import json
import math
import requests
import urllib.request
from datetime import datetime
from data_analytics import db_interface as db
import os
from sklearn.linear_model import LinearRegression

# ignore warnings
import warnings

warnings.filterwarnings('ignore')


cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
path = cwd[:-7]

# load environment
database = "postgres"
user = "postgres"
password = "YZuB%F34qYSbpp7J"
host = "group-10-dublin-bus.cu4ammu8tjpf.eu-west-1.rds.amazonaws.com"
port = 5432
weather_api_key = "86baa129046e5cbaeb16af074356e579"

def get_weather_from_db():
    """returns a tuple of the 'current' weather data from out postgres database."""

    sql = db.construct_sql(table_name="weather_data_current", query_type="select_all")
    
    data = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)
    
    return data[0]


def time_group_function(row):
    """given a time in seconds after midnight, returns a "time_group". a time_group is a portion of the day.

        We have split the day into 29 portions.
        These portions are 60 minutes at off peak travel times and 30 minutes during peak times"""
    row = int(row)
    time_group_departure = []
    if row < 0:
        print("Error - negative time stamp")
    # from 00:00 to 01:00
    elif row <= 3600 or (row > 86400 and row <= 90000):
        time_group_departure.append('0')
    # from 01:00 to 02:00
    elif row > 3600 and row <= 7200 or (row > 90000 and row <= 93600):
        time_group_departure.append('1')
    # from 02:00 to 03:00
    elif row > 7200 and row <= 10800:
        time_group_departure.append('2')
    # from 03:00 to 04:00
    elif row > 10800 and row <= 14400:
        time_group_departure.append('3')
    # from 04:00 to 05:00
    elif row > 14400 and row <= 18000:
        time_group_departure.append('4')

    # from 05:00 to 06:00
    elif row > 18000 and row <= 21600:
        time_group_departure.append('5')
    # from 06:00 to 07:00
    elif row > 21600 and row <= 25200:
        time_group_departure.append('6')
    # from 07:00 to 07:30
    elif row > 25200 and row <= 27000:
        time_group_departure.append('7')
    # from 07:30 to 08:00
    elif row > 27000 and row <= 28800:
        time_group_departure.append('8')
    # from 08:00 to 08:30
    elif row > 28800 and row <= 30600:
        time_group_departure.append('9')
    # from 08:30 to 09:00
    elif row > 30600 and row <= 32400:
        time_group_departure.append('10')
    # from 09:00 to 10:00
    elif row > 32400 and row <= 36000:
        time_group_departure.append('11')
    # from 10:00 to 11:00
    elif row > 36000 and row <= 39600:
        time_group_departure.append('12')
    # from 11:00 to 12:00
    elif row > 39600 and row <= 43200:
        time_group_departure.append('13')
    # from 12:00 to 13:00
    elif row > 43200 and row <= 46800:
        time_group_departure.append('14')

    # from 13:00 to 14:00
    elif row > 46800 and row <= 50400:
        time_group_departure.append('15')
    # from 14:00 to 15:00
    elif row > 50400 and row <= 54000:
        time_group_departure.append('16')
    # from 15:00 to 16:00
    elif row > 54000 and row <= 57600:
        time_group_departure.append('17')
    # from 16:00 to 16:30
    elif row > 57600 and row <= 59400:
        time_group_departure.append('18')
    # from 16:30 to 17:00
    elif row > 59400 and row <= 61200:
        time_group_departure.append('19')

    # from 17:00 to 17:30
    elif row > 61200 and row <= 63000:
        time_group_departure.append('20')
    # from 17:30 to 18:00
    elif row > 63000 and row <= 64800:
        time_group_departure.append('21')
    # from 18:00 to 18:30
    elif row > 64800 and row <= 66600:
        time_group_departure.append('22')
    # from 18:30 to 19:00
    elif row > 66600 and row <= 68400:
        time_group_departure.append('23')
    # from 19:00 to 20:00
    elif row > 68400 and row <= 72000:
        time_group_departure.append('24')

    # from 20:00 to 21:00
    elif row > 72000 and row <= 75600:
        time_group_departure.append('25')
    # from 21:00 to 22:00
    elif row > 75600 and row <= 79200:
        time_group_departure.append('26')
    # from 22:00 to 23:00
    elif row > 79200 and row <= 82800:
        time_group_departure.append('27')
    # from 23:00 to 24:00
    elif row > 82800 and row <= 86400:
        time_group_departure.append('28')

    return time_group_departure[0]


def get_active_columns(test):
    """Returns a list of the categorical columns in a given test dataframe that are "positive".

    For example the test_dataframe fed to the pickle might have columns for the categorical feature "DAYOFWEEK" but in any given
    instance of the dataframe only one of those 7 will be positive. If the day in question is a Monday then DAYOFWEEK_0 will be "positive" 
    and the other six will be "negative". The same for weather_main, weather_description, MONTH and TIME_GROUP"""

    active_columns = []

    # for each column in the dataframe...
    for column in test:
        # ...get a string of the "result" of the column - ie. "broken clouds" or "12" and then...
        ending_raw = str(list(test[column].unique()))

        # ...use a series of nonsense variables to remove unwanted characters and get an "ending"
        fee = ending_raw.replace("[", '')
        fi = fee.replace("'", '')
        ending_final = fi.replace("]", '')

        # append that "ending" to the string of that column title to get a string that mimics the format of the one hot encoding variables
        string = str(column) + "_" + ending_final

        # append that string to the list
        active_columns.append(string)

    # return the list
    return active_columns


def generate_test_dataframe(route, direction, date, time):
    """Returns a dataframe with the user entered trip details if given the route, direction, date and time
    
    This function is called from the generate_predictions function and in turn calls the get_weather_from_db function, 
    the time_group_function  and the get_active_columns function
    The list of columns in the dataframe varies per route, and the list of columns is stored in a json format on the database
    Continuous features are added to that dataframe directly, whereas categorical features that need to be one hot encoded for
    are added to a temporary dataframe.
    The get_active_columns function returns a list of which categorical features in the dataframe needed to be marked 1 instead of 0."""
    # get weather from database
    weather = get_weather_from_db()
    # extract required parameters
    temp = weather[2]
    feels_like = weather[3]
    main = weather[6]
    description = weather[7]
    wind_speed = weather[4]
    wind_deg = weather[5]
    rain = weather[8]

    # create empty dataframe with correct headings from templates generated from list of columns from the datasets used to train the linear regression models

    template_name = str(route) + "_" + str(direction)
    # construct sql query
    sql = db.construct_sql(table_name="model_features", query_type="select_where", column_names=["features"], data={"id": template_name})
    # execute sql query

    response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)[0][0]
  
    # make a single row to contain the test data and put 0 in every column.
    row = [0] * len(response)
    # create the dataframe
    test_frame = pd.DataFrame([row], columns=response)

    # now forget about the test dataframe for a while and pop my user entered data into a temporary dataframe...
    data = {"DAYOFSERVICE": [date], "TIME": [time]}
    temp_dataframe = pd.DataFrame(data)

    # ...add in the categorical features from the weather api request...
    temp_dataframe['weather_main'] = main
    temp_dataframe['weather_description'] = description

    # ...converting date to date format from string
    date_list = []
    for row in temp_dataframe['DAYOFSERVICE']:
        x = datetime.strptime(row, '%Y-%m-%d')
        date_list.append(x)

    # add that date in date format to the temporary dataframe...
    temp_dataframe['DAYOFSERVICE'] = date_list

    # ...creating month and day of the week feature from that date...
    temp_dataframe['MONTH'] = temp_dataframe['DAYOFSERVICE'].dt.month
    temp_dataframe['DAYOFWEEK'] = temp_dataframe['DAYOFSERVICE'].dt.dayofweek

    # ...creating Time Group Feature from the time....
    time_group_departure = time_group_function(time)
    temp_dataframe['TIME_GROUP'] = time_group_departure

    # ...drop the date and time features we don't need...
    temp_dataframe = temp_dataframe.drop(columns=['DAYOFSERVICE', 'TIME'])

    # remember that test dataframe we created at the beginning... well, now we...
    # use the get_active_columns function to figure out the names of the categorical columns in the test dataframe that need to be
    # encoded to 1 (instead of 0) and then...
    active_columns = get_active_columns(temp_dataframe)

    # ... itterate through this one line test dataframe and if the column is in the list of active columns...
    # ...assign the value of that column at index 0 (because there will only ever be one line) as 1
    for column, row in test_frame.items():
        if column in active_columns:
            row.iloc[0] = 1

    # add the continuous features directly to the test dataframe
    test_frame['temp'] = temp
    test_frame['feels_like'] = feels_like
    test_frame['wind_speed'] = wind_speed
    test_frame['wind_deg'] = wind_deg
    test_frame['rain'] = rain

    # and return the test dataframe to the pickled linear regression
    return test_frame


def get_indices(startstop, endstop, dictionary, order_segment_list):
    """Returns the indices of the users boarding and alighting stop in an ordered list of the stops on that route.
    
    In this code the dictionary in question will be a dictionary with stop segments as keys and the proportion of the total journey
    that this stop represents"""

    indices = []
    for key, value in dictionary.items():
        # split the key into the two stop numbers that form it
        dict_stops = key.split("_")
        # if the first stop number is the users boarding stop...
        if dict_stops[0] == str(startstop):
            # its the start index so add it to the list
            start_index = order_segment_list.index(key)
            indices.append(start_index)
        # if the second stop number is the users alighting stop...
        if dict_stops[1] == str(endstop):
            # its the end index so add it to the list
            end_index = order_segment_list.index(key)
            indices.append(end_index)
    # return the list
    return indices


def segment_calculation(startstop, endstop, dictionary):
    """not used since change to databse, will keep for now in case we use as a backup"""

    total = 0
    count = 0

    order_segment_list = []
    # this part uses the dictionary keys in the order they occur in this dictionary at this point in time
    # to create a list of the segments in order.
    # I am of course aware that order in dictionaries can't be relied upon, but it doesn't really matter in this case,
    # as it's only being used to itterate through itself
    # I needed the exact list as it is in this dictionary, now, rather than using the master list of ordered stops
    # to protect against missing segments.
    order_segments_dict = (dictionary.keys())
    for i in order_segments_dict:
        order_segment_list.append(i)

    # get the indices of the users start and end stop in the above list
    indices = get_indices(startstop, endstop, dictionary, order_segment_list)

    #
    for i in range(indices[0], indices[1] + 1):
        value = dictionary[order_segment_list[i]]
        # this is to handle the odd NaN value in our proporitons datasets. NaNs occur at an average incidence
        # of 0.12% in the data.
        if math.isnan(value):
            pass  # if a NaN is present we simply delete that segment from calculations as if it didn't exist,
            # so there will be a small loss of accuracy
        else:
            total += value

    return total


def quickanddirty(route, direction, startstop, endstop):
    """Returns proportion of the total journey that the user takes simply as percentage of how many of the stops on the route they travelled
        
        I don't like this function, because I don't see the point of training a linear regression model, and then using a blunt object like this to 
        allocate the proportion. It is simply here as a failsafe. The main segment_calculation function contains its own checks and failsafes.
        It can handle a NaN value in the proportions or a missed/skippedd segment... however...
        One situation when this function may be needed is for example... the 41 bus route is 24 hours now and wasn't in 2018, so...
        If linear regression will manage to return a 3am prediction... but the proportion function would fail as the 3am time_group is empty
        However, that isn't the worst thing in the world... because at 3am a simple average is probably more accurate than at 6pm on a weekday"""

    # get the master list of ordered stops
    f = open(path + 'web_app/journeyplanner/static/journeyplanner/ordered_stops_main.json')
    ordered_stop_data = json.load(f)
    
    # get the stops for the subroutes on that route as a dictionary
    ordered_stop_data_route = ordered_stop_data[str(route)]
    for key, value in ordered_stop_data_route.items():
        # for the main (or majority subroute) in the given direction on that route...
        if ordered_stop_data_route[key]['direction'] == int(direction) and ordered_stop_data_route[key]['main'] == True:
            # find how many stops on the route, how many the user travelled, divide the later by the former
            main_route_stops = ordered_stop_data_route[key]['stops']
            main_route_length = len(main_route_stops)
            user_route_length = len(main_route_stops[main_route_stops.index(int(startstop)):main_route_stops.index(int(endstop)) + 1])
            proportion = user_route_length / main_route_length
            return proportion


def get_proportion(route, direction, startstop, endstop, weekday, month, time_group):
    """returns a proportion representing the amount of the total bus route journey that the users journey represents
        
        It will first attempt to do this using calculated proportions for that day of the week, month and time_group, but will resort to 
        a simple percentage of the amount of the stops travelled compared to the amount of stops there are"""

    # dictionaries for use finding the relevant section of the code in the database
    days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3: "Thursday", 4: "Friday", 5: "Saturday", 6: "Sunday"}
    months = {1: "January", 2: "Febuary", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August",
              9: "September", 10: "October", 11: "November", 12: "December"}
    times = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "11",
             12: "12", 13: "13", 14: "14", 15: "15", 16: "16", 17: "17", 18: "18", 19: "19", 20: "20", 21: "21",
             22: "22", 23: "23", 24: "24", 25: "25", 26: "26", 27: "27", 28: "28"}

    # call proportions file in dictionary format - this proportions file returns a calculated average based on previous journies for a given...
    # ...month, week and time_group...
    try:
    # construct sql query
        table_name = "route_%s_%s_proportions" % (route.lower(), direction)
        sql_values = db.construct_sql(table_name=table_name, query_type="select_where",data={"month": months[month], "weekday": days[weekday], "timegroup": str(time_group)})
        
        sql_keys = db.construct_sql(table_name=table_name, query_type="attr_names")
       
        
        response_values = db.execute_sql(sql_values, database, user, password, host, port, retrieving_data=True)[0]
        
        response_keys = db.execute_sql(sql_keys, database, user, password, host, port, retrieving_data=True)
        
        list_of_values = list(response_values[3:])
        list_of_keys = list(response_keys[3:])
    
        for item in list_of_keys:
            if list_of_keys.index(item) != len(list_of_keys)-1:
                splitsegment = str(item).split("_")
                first_stop_segment = str(item).split("_")[0][3:]
                last_stop_segment = str(item).split("_")[1][:-2]
    
                if startstop == first_stop_segment:
                    index1 = list_of_keys.index(item)
                if endstop == last_stop_segment:
                    index2 = list_of_keys.index(item)

        total = 0

        for i in range(index1, index2 + 1):
            if list_of_values[i] is not None: # this is to handle the odd NaN value in our proporitons datasets. 
        # NaNs occur at an average incidence
        # of 0.12% in the data.
                value = list_of_values[i]
                total += value
        proportion = total
        if proportion > 0:
            return proportion
        else:
            print("Unable to access proportions data, using simple percentage of route")
            proportion = quickanddirty(route, direction, startstop, endstop)
            return proportion

    # otherwise simply return the percentage of the number of stops a user is travelling (*eyeroll*)
    except:
        print("Unable to access proportions data, using simple percentage of route")
        proportion = quickanddirty(route, direction, startstop, endstop)
    return proportion


def generate_prediction(route, startstop, endstop, date, time, direction):
    print("From generate prediction: ", route, startstop, endstop, date, time, direction)
    """It returns the users estimated journey time in minutes. It is the main function in the script. It is the one called from the front end, and calls all the other functions either directly or indirectly
    Takes route, the users boarding stop, the users alighting stop, the date, time and direction as parameters. 
    """
    # calls a function which generates a test dataframe from the route number, the direction, the date and the time.
    test = generate_test_dataframe(route, direction, date, time)
    # loads the correct linear regression pickle using the route and direction
    pickle_file = path + "web_app/data_analytics/pickles_new/" + str(route) + "_direction" + str(direction) + ".pickle"
    pickle_in = open(pickle_file, 'rb')
    linear_regression = pickle.load(pickle_in)

    # get the prediction from the pickle using the test dataframe generated above
    prediction = linear_regression.predict(test)
    print("Prediction from model: ", int(prediction[0]))

    # get month, day_of_the_week and time_group from the date and time, these are needed for calculating the proportion of the total
    # journey that the users trip represents. 
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')
    weekday = date_time_obj.weekday()
    month = date_time_obj.month
    time_group = time_group_function(time)

    # get the proportion using the get_proportion
    proportion = get_proportion(route, direction, startstop, endstop, weekday, month, int(time_group))

    # get proportion and multiply by the prediction
    result = proportion * prediction[0]
    print("Users proportion: ", proportion)
    print("Users estimated journeytime: ", int(result))
    minutes = int(result) // 60
    return minutes
