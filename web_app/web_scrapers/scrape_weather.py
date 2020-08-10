import requests
import csv
import os
import pytz
import json
import sys
from dotenv import load_dotenv, find_dotenv
from web_app.db_interface import db_interface as db
from datetime import datetime

# locate & read .env file
load_dotenv(find_dotenv())

database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
weather_api = os.environ.get("weather_key")


def scrape_weather(**kwargs):
    """retrieve current or forecast weather data from openweathermap.org"""

    # define valid types of request to the API
    req_types = ["weather", "forecast"]

    # default to current weather request
    if "req_type" in kwargs:
        req = kwargs["req_type"]
        if req not in req_types:
            req = "weather"
    else:
        req = "weather"

    if "city" in kwargs:
        city = kwargs["city"]
    else:
        city = "Dublin,,372"                     # 372 is the ISO 3166 Country Code for Ireland

    if "key" in kwargs:
        api_key = kwargs["key"]
    else:
        try:
            api_key = weather_api
        except Exception as e:
            print("Error: no api key supplied")
            print(e)
            return e

    url = "http://api.openweathermap.org/data/2.5/%s?q=%s&appid=%s&units=metric" % (req, city, api_key)
    print(url)

    # get weather info and convert to python dict
    response = requests.get(url)
    out_dict = json.loads(response.text)

    return out_dict


def flatten_dict(some_dict):
    """Takes a parent dictionary containing multiple nested dictionaries and returns a
    single non-nested dictionary combining all keys from the root dictionary with all
    keys contained in nested dictionaries. This is a recursive function!!"""

    out_dict = {}                                            # init empty dict to hold output

    keys = list(some_dict.keys())

    for i in keys:

        if type(some_dict[i]) == dict:                      # if key is nested dict; call flatten_dict(key)
            some_dict[i] = prefix_keys(some_dict[i], i)
            out_dict.update(flatten_dict(some_dict[i]))

        elif type(some_dict[i]) == list:                    # else if key is nested list; call flatten_dict(key)

            temp_dict = {}                                  # convert list to dict
            for j in range(len(some_dict[i])):
                temp_dict["%d" % j] = some_dict[i][j]

            some_dict[i] = prefix_keys(temp_dict, i)
            out_dict.update(flatten_dict(some_dict[i]))

        else:                                               # else; copy key-value to output dict
            out_dict[i] = some_dict.pop(i)

    return out_dict


def prefix_keys(some_dict, prefix):
    """returns a dictionary with a prefix to the name of each key in the top level of the dictionary"""

    keys = list(some_dict.keys())
    temp_dict = {}
    for key in keys:
        temp_dict[prefix + "_" + key] = some_dict.pop(key)
        some_dict.update(temp_dict)
    return some_dict


def write_to_csv(file_path, some_dict):
    """append the values within a passed dictionary to the corresponding fields in the passed csv file"""

    # if file exists append to existing file
    if os.path.isfile(file_path):
        with open(file_path, "a") as file:
            writer = csv.DictWriter(file, some_dict.keys())
            writer.writerow(some_dict)

    # else create a new file with header row
    else:
        with open(file_path, "w") as file:
            writer = csv.DictWriter(file, some_dict.keys())
            writer.writeheader()
            writer.writerow(some_dict)


def main(**kwargs):

    if "forecast" in kwargs and type(kwargs["forecast"] is bool):
        get_forecast = kwargs["forecast"]
    else:
        get_forecast = False

    # retrieve weather data
    if get_forecast:
        weather_data = dict(scrape_weather(req_type="forecast"))["list"]
        table_name = "weather_data_forecast"
    else:
        weather_data = [dict(scrape_weather())]
        table_name = "weather_data_current"

    for entry in weather_data:
        store_weather(entry, table_name)

    #sql = "SELECT COUNT(DISTINCT date) FROM %s" % table_name
    #print(sql)
    #response = db.execute_sql(sql, database=database, user=user, password=password,
    #                          host=host, port=port, retrieveing_data=True)

    #print(response)
    #if get_forecast:
    #    if len(response) > 40:
    #        clear_oldest(table_name=table_name)
    #elif len(response) > 1:
    #    clear_oldest(table_name=table_name)

    clear_oldest(table_name=table_name)


def store_weather(weather_data, table_name):

    weather_data = flatten_dict(weather_data)

    # if there's no measurement for rainfall assume rainfall of 0
    if "rain_1h" not in weather_data:
        # if there's a 3 hour measurement for rainfall (ie. for forecast data) - use this in place of 1 hr value
        if "rain_3h" in weather_data:
            weather_data["rain_1h"] = weather_data["rain_3h"]
        else:
            weather_data["rain_1h"] = 0.0

    # if there's no timezone offset value then create one
    if "timezone" not in weather_data:
        gmt = pytz.timezone("GMT")
        dt = pytz.utc.localize(datetime.utcfromtimestamp(weather_data["dt"]))
        weather_data["timezone"] = dt.astimezone(gmt).utcoffset().total_seconds()

    # select only desired fields from raw data
    data = {"date": datetime.fromtimestamp(weather_data["dt"]).strftime("%Y-%m-%d %H:%M:%S"),
            "timezone": weather_data["timezone"],
            "temp": weather_data["main_temp"],
            "feels_like": weather_data["main_feels_like"],
            "wind_speed": weather_data["wind_speed"],
            "wind_deg": weather_data["wind_deg"],
            "weather_main": weather_data["weather_0_main"],
            "weather_description": weather_data["weather_0_description"],
            "rain": weather_data["rain_1h"]
            }

    # push new data to database...
    try:
        sql_query = db.construct_sql(query_type="insert", table_name=table_name, data=data)
        db.execute_sql(sql_query, database=database, user=user, password=password, host=host, port=port,
                       retrieveing_data=False)
    except Exception as e:
        try:
            sql_query = db.construct_sql(query_type="update", table_name=table_name,
                                         data=data, predicates={"date": data["date"]})
            db.execute_sql(sql_query, database=database, user=user, password=password,
                           host=host, port=port, retrieveing_data=False)
            print("Update successful")
        except Exception as e:
            print(e)
            return e


def clear_oldest(**kwargs):

    if "table_name" in kwargs:
        table_name = kwargs["table_name"]
    else:
        print("Error: no table specified")

    if "col" in kwargs:
        col = str(kwargs["col"])
    else:
        col = "date"

    # get the 'oldest' record in the table
    sql = """SELECT %s FROM %s ORDER BY %s ASC LIMIT 1""" % (col, table_name, col)
    try:
        response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)
    except Exception as e:
        return e

    sql = """DELETE FROM %s WHERE %s = '%s'::TIMESTAMP""" % (table_name, col, str(str(response[0][0])))
    try:
        db.execute_sql(sql, database, user, password, host, port, retrieving_data=False)
    except Exception as e:
        return e


if __name__ is "__main__":

    # check for key-word arguments from bash

    if sys.argv[1] == "forecast":
        main(forecast=True)
    else:
        main()
