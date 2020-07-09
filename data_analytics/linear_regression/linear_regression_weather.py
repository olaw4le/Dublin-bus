import pandas as pd
import pickle
import requests, json
import urllib.request
from datetime import datetime
import db_interface as db
import os
from dotenv import load_dotenv
#from sklearn.linear_model import LinearRegression

# load environment variables !!
load_dotenv()

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
    database = os.getenv("database")
    user = os.getenv("user")
    password = os.getenv("password")
    host = os.getenv("host")
    port = os.getenv("port")

    sql = db.construct_sql(table_name="weather_data_current", query_type="select_all")
    data = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)

    return data


def generate_preditction(route, startstop, endstop, date, time, direction):
    #what do I want to do....
    #I want to get the weather(current)
    #ultimately this will be coming from a database...
    #api request
    url = "http://api.openweathermap.org/data/2.5/weather?id=2964574&units=metric&appid=60277b654b7eab1a458f410bb214f606"
    response = requests.get(url)
    x = response.json()
    print(x)
    weather = x['weather']
    foo = weather[0]
    main = foo['main']
    description = foo['description']

    bar = x['main']
    temp = bar['temp']
    feels_like = bar['feels_like']

    wind = x['wind']
    speed = wind['speed']
    deg = wind['deg']

    print (main, description, temp, feels_like, speed, deg)

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
generate_preditction(route, 1234, 2345, "2020-14-03", 12345, direction)
