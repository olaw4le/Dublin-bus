import requests
import csv
import os.path
import sys
import json
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

weather_api = os.environ.get("WEATHER")


def get_weather_data():
    """retrieve current weather data from openweathermap.org"""

    city = "Dublin,,372"                                # 372 is the ISO 3166 Country Code for Ireland
    api_key = weather_api

    url = "http://api.openweathermap.org/data/2.5/weather?q=%s&appid=%s" % (city, api_key)

    # get weather info and convert to python dict
    response = requests.get(url)
    out_dict = json.loads(response.text)

    return out_dict


def flatten_dict(some_dict):
    """Takes a parent dictionary containing multiple nested dictionaries and returns a
    single non-nested dictionary combining all keys from the root dictionary with all
    keys contained in nested dictionaries. If This is a recursive function!!"""

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


def main(file_path):

    # get & format data from openweathermaps.org
    data = flatten_dict(get_weather_data())

    # check for missing fields and populate missing fields with empty strings
    columns = ["coord_lon", "coord_lat", "weather_0_id", "weather_0_main", "weather_0_description",
               "weather_0_icon", "base" , "main_temp", "main_feels_like", "main_temp_min", "main_temp_max",
               "main_pressure", "main_humidity", "visibility", "wind_speed", "wind_deg", "clouds_all",
               "rain_1h", "rain_3h", "snow_1h", "snow_3h", "dt", "sys_type", "sys_id", "sys_country",
               "sys_sunrise", "sys_sunset", "timezone", "id", "name", "cod"]

    for field in columns:
        if field not in data.keys():
            data[field] = ""

    # append data to the file path
    write_to_csv(file_path, data)


if __name__ == "__main__":

    if len(sys.argv) > 1:
        out_file = sys.argv[1]
    else:
        out_file = "openweatherdata_scraped.csv"

    main(out_file)

