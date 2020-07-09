import pandas as pd
import pickle
import requests, json
import urllib.request
from datetime import datetime
import db_interface as db
import os
from dotenv import load_dotenv
import dotenv
#from sklearn.linear_model import LinearRegression

# load environment variables !!

# ignore warnings
import warnings
warnings.filterwarnings('ignore')
route = "84A"
direction = 1


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


def generate_preditction(route, startstop, endstop, date, time, direction):
    #what do I want to do....
    #I want to get the weather(current)
    #ultimately this will be coming from a database...
    #api request
    #url = "http://api.openweathermap.org/data/2.5/weather?id=2964574&units=metric&appid=60277b654b7eab1a458f410bb214f606"
    
    x = get_weather_from_db()
    
    temp = x[2]
    feels_like = x[3]
    main = x[6]
    description = x[7]
    speed = x[4]
    #in m/s
    deg = x[5]
    rain = x[8]

    print (main, description, temp, feels_like, speed, deg, rain)

    #construct a dataframe to match the linear_regression weather one.
    #test = "dataframe"
    #find my pickle
    #pickle_file = "/pickles/" + str(route) + "_direction" + str(direction) + ".pickle"
    #pickle_in = open(pickle_file, 'rb')
    #linear_regression = pickle.load(pickle_in)

    #get the prediction

    #prediction = linear_regression.predict(test)

    #get the proportion

    #read in Milo csv
    #get proportion
    # result = answer * prediciton

    #return result
get_weather_from_db()
generate_preditction(route, 1234, 2345, "2020-14-03", 12345, direction)
