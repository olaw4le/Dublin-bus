import pandas as pd
import pickle
import json
import requests, json
import urllib.request
from datetime import datetime
import db_interface as db
import os
from dotenv import load_dotenv
import dotenv
from sklearn.linear_model import LinearRegression

# ignore warnings
import warnings
warnings.filterwarnings('ignore')

def get_weather_from_db():
    """
    returns a tuple of the 'current' weather data from out postgres database.
    returned values:
    date: datetime (may return a tuple of ints)
    timezone offset: int
    temp: float
    feels_like (temp): float
    wind_speed: float
    wind_deg (direction): int (in range 0:360)
    weather_main: string
    weather_description: string
    rain_1h: float
    """

    # load environment
    database="postgres"
    user="postgres"
    password="YZuB%F34qYSbpp7J"
    host="group-10-dublin-bus.cu4ammu8tjpf.eu-west-1.rds.amazonaws.com"
    port=5432
    weather_api_key="86baa129046e5cbaeb16af074356e579"
    
    sql = db.construct_sql(table_name="weather_data_current", query_type="select_all")
    data = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)

    return data[0]
def time_group_function(row):
            time_group_departure = []
    #for row in test['TIME']:
            #row = int(row)
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

            return time_group_departure[0]

def get_active_columns(test):
    active_columns = []
    for column in test:
        ending_raw = str(list(test[column].unique()))
        fee = ending_raw.replace("[", '')
        fi = fee.replace("'", '')
        ending_final = fi.replace("]", '')
        string = str(column) + "_" + ending_final
        active_columns.append(string)
    return active_columns

def generate_test_dataframe(route, direction, date, time):
    #get weather from database
    weather = get_weather_from_db()

    #extract required parameters
    temp = weather[2]
    feels_like = weather[3]
    main = weather[6]
    description = weather[7]
    wind_speed = weather[4]
    # in m/s
    wind_deg = weather[5]
    rain = weather[8]
    #create empty dataframe with correct headings
    
    f = open('/Users/laura/Desktop/Trimester_3/research-project/data_analytics/linear_regression/result_templates.json',) 
  
    # returns JSON object as  
    # a dictionary 
    templates = json.load(f) 
    template_name = str(route) + "_" + str(direction)
    features = templates[template_name]
    #print(features)
    row = [0]*len(features)

    test_frame = pd.DataFrame([row],columns=features)

    
    #pop my user entered data into a dataframe
    data = {"DAYOFSERVICE":[date], "TIME":[time]}
    test = pd.DataFrame(data)

    #add in the weather
    test_frame['temp']= temp
    test_frame['feels_like'] = feels_like
    test_frame['wind_speed'] = wind_speed
    test_frame['wind_deg'] = wind_deg
    test_frame['rain'] = rain
    test['weather_main'] = main
    test['weather_description'] = description

    #converting date to date format from string
    date_list = []

    for row in test['DAYOFSERVICE']:
            x = datetime.strptime(row, '%Y-%m-%d')
            date_list.append(x)

    test['DAYOFSERVICE'] = date_list

    #creating month and day of the week feature
    test['MONTH'] = test['DAYOFSERVICE'].dt.month
    test['DAYOFWEEK'] = test['DAYOFSERVICE'].dt.dayofweek


    #Creating Time Group Feature
    time_group_departure = time_group_function(time)


    test['TIME_GROUP'] = time_group_departure
    
    
    #drop the date and time features we don't need

    test = test.drop(columns=['DAYOFSERVICE', 'TIME'])
    active_columns = []

    active_columns = get_active_columns(test)
    

    for word in active_columns:
        if active_columns in list(test_frame.columns):
            test_frame[column] = [1]
    
    return test_frame


def get_proportion(route, direction, startstop, endstop, weekday, month, time_group):
        days = {0: "Monday", 1: "Tuesday", 2: "Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
        months = {1: "January", 2: "Febuary", 3: "March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}
        #call proportions file
        proportions_name = str(route) + "_" + str(direction) + "_proportions.json"
        file_path = '/Users/laura/Desktop/Trimester_3/research-project/data_analytics/linear_regression/Proportions_files/' + proportions_name

        f = open(file_path) 
        # returns JSON object as  
        # a dictionary 
        proportions_json = json.load(f)
        proportions_json1 = proportions_json['Day_of_week']
        weekday_json = proportions_json1[days[weekday]]
        month_json = weekday_json[months[month]]
        time_group_json = month_json[str(time_group)]
        stats = time_group_json['stats']
        proportions = stats['proportions']
        #print(proportions)

        #call the ordered list
        proportion = 0
        temp = startstop
        for key, value in proportions.items():
             x = key.split("_")
             print(x[0])
             if x[0] == str(temp):
                proportion += value
                temp = x[1]
                if temp == str(endstop):
                        print(proportion)
                        return proportion



def get_route_file(route):
    # master dictionary of route numbers and their corresponding master files
    master_route_dict = {"18": "Eighteen_Master.csv", "17": "Seventeen_Master.csv", "84A": "EightyFourA_Master.csv",
                         "70D": "SeventyD_Master.csv", "84X": "EightyFourX_Master.csv",
                         "75": "SeventyFive_Master.csv", "84": "EightyFour_Master.csv",
                         "79A": "SeventyNineA_Master.csv", "83A": "EightyThreeA_Master.csv",
                         "79": "SeventyNine_Master.csv", "83": "EightyThree_Master.csv",
                         "77A": "SeventySevenA_Master.csv", "11": "Eleven_Master.csv",
                         "77X": "SeventySevenX_Master.csv", "15A": "FifteenA_Master.csv",
                         "76A": "SeventySixA_Master.csv", "15B": "FifteenB_Master.csv",
                         "76": "SeventySix_Master.csv", "15D": "FifteenD_Master.csv", "70": "Seventy_Master.csv",
                         "15": "Fifteen_Master.csv", "16C": "SixteenC_Master.csv", "54A": "FiftyFourA_Master.csv",
                         "16D": "SixteenD_Master.csv", "16": "Sixteen_Master.csv", "51D": "FiftyOneD_Master.csv",
                         "68A": "SixtyEightA_Master.csv", "51X": "FiftyOneX_Master.csv",
                         "68X": "SixtyEightX_Master.csv", "56A": "FiftySixA_Master.csv",
                         "68": "SixtyEight_Master.csv", "53": "FiftyThree_Master.csv",
                         "65B": "SixtyFiveB_Master.csv", "40B": "FortyB_Master.csv", "65": "SixtyFive_Master.csv",
                         "40D": "FortyD_Master.csv", "69X": "SixtyNineX_Master.csv", "40E": "FortyE_Master.csv",
                         "69": "SixtyNine_Master.csv", "45A": "FortyFiveA_Master.csv", "61": "SixtyOne_Master.csv",
                         "44B": "FortyFourB_Master.csv", "67X": "SixtySevenX_Master.csv",
                         "44": "FortyFour_Master.csv", "67": "SixtySeven_Master.csv", "49": "FortyNine_Master.csv",
                         "66A": "SixtySixA_Master.csv", "41A": "FortyOneA_Master.csv",
                         "66B": "SixtySixB_Master.csv", "41C": "FortyOneC_Master.csv",
                         "66X": "SixtySixX_Master.csv", "41D": "FortyOneD_Master.csv", "66": "SixtySix_Master.csv",
                         "41X": "FortyOneX_Master.csv", "63": "SixtyThree_Master.csv", "41": "FortyOne_Master.csv",
                         "13": "Thirteen_Master.csv", "47": "FortySeven_Master.csv",
                         "38A": "ThirtyEightA_Master.csv", "46A": "FortySixA_Master.csv",
                         "38B": "ThirtyEightB_Master.csv", "46E": "FortySixE_Master.csv",
                         "38D": "ThirtyEightD_Master.csv", "43": "FortyThree_Master.csv",
                         "38": "ThirtyEight_Master.csv", "42D": "FortyTwoD_Master.csv",
                         "39A": "ThirtyNineA_Master.csv", "42": "FortyTwo_Master.csv",
                         "39X": "ThirtyNineX_Master.csv", "40": "Forty_Master.csv", "39": "ThirtyNine_Master.csv",
                         "4": "Four_Master.csv", "31A": "ThirtyOneA_Master.csv", "14C": "FourteenC_Master.csv",
                         "31B": "ThirtyOneB_Master.csv", "14": "Fourteen_Master.csv",
                         "31D": "ThirtyOneD_Master.csv", "31": "ThirtyOne_Master.csv", "9": "Nine_Master.csv",
                         "37": "ThirtySeven_Master.csv", "185": "OneEightyFive_Master.csv",
                         "33A": "ThirtyThreeA_Master.csv", "184": "OneEightyFour_Master.csv",
                         "33B": "ThirtyThreeB_Master.csv", "111": "OneEleven_Master.csv",
                         "33D": "ThirtyThreeD_Master.csv", "151": "OneFiftyOne_Master.csv",
                         "33E": "ThirtyThreeE_Master.csv", "150": "OneFifty_Master.csv",
                         "33": "ThirtyThree_Master.csv", "145": "OneFortyFive_Master.csv",
                         "32X": "ThirtyTwoX_Master.csv", "142": "OneFortyTwo_Master.csv",
                         "32": "ThirtyTwo_Master.csv", "140": "OneForty_Master.csv",
                         "25A": "TwentyFiveA_Master.csv", "114": "OneFourteen_Master.csv",
                         "25B": "TwentyFiveB_Master.csv", "104": "OneOFour_Master.csv",
                         "25D": "TwentyFiveD_Master.csv", "102": "OneOTwo_Master.csv",
                         "25X": "TwentyFiveX_Master.csv", "116": "OneSixteen_Master.csv",
                         "25": "TwentyFive_Master.csv", "161": "OneSixtyOne_Master.csv",
                         "29A": "TwentyNineA_Master.csv", "130": "OneThirty_Master.csv",
                         "27A": "TwentySevenA_Master.csv", "123": "OneTwentyThree_Master.csv",
                         "27B": "TwentySevenB_Master.csv", "122": "OneTwentyTwo_Master.csv",
                         "27X": "TwentySevenX_Master.csv", "120": "OneTwenty_Master.csv",
                         "27": "TwentySeven_Master.csv", "1": "One_Master.csv", "26": "TwentySix_Master.csv",
                         "7A": "SevenA_Master.csv", "270": "TwoSeventy_Master.csv", "7B": "SevenB_Master.csv",
                         "238": "TwoThirtyEight_Master.csv", "7D": "SevenD_Master.csv",
                         "239": "TwoThirtyNine_Master.csv", "7": "Seven_Master.csv",
                         "236": "TwoThirtySix_Master.csv", "17A": "SeventeenA_Master.csv",
                         "220": "TwoTwenty_Master.csv", "59": 'FiftyNine_Master.csv', "41B": 'FortyOneB_Master.csv',
                         '118': 'OneEighteen_Master.csv', '33X': 'ThirtyThreeX_Master.csv'}

    # calling the master route file for the given request
    route_file = master_route_dict[str(route)]
    file = "~/Desktop/Master-Route-Files/" + route_file
    df = pd.read_csv(file, keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
    return df



def generate_preditction(route, startstop, endstop, date, time, direction):

    df = get_route_file(route)
    test = generate_test_dataframe(route, direction, date, time)
    print(test)


    #find my pickle
    pickle_file = "/Users/laura/Desktop/Trimester_3/research-project/data_analytics/linear_regression/pickles/" + str(route) + "_direction" + str(direction) + ".pickle"
    pickle_in = open(pickle_file, 'rb')
    linear_regression = pickle.load(pickle_in)

    #get the prediction

    prediction = linear_regression.predict(test)
    print(prediction)

    #get month, day_of_the_week and time_group
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')
    weekday = date_time_obj.weekday()
    month = date_time_obj.month
    time_group = time_group_function(time)
    

    #get the proportion
    answer = get_proportion(route, direction, startstop, endstop, weekday, month, 8)
    
    #get proportion
    result = answer * prediction[0]
    print(result)
    return result

generate_preditction(151, 2279, 301, "2020-07-11", 12345, 1)
