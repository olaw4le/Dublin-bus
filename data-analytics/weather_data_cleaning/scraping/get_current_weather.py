import requests
import csv
import os.path
import sys
import json
from dotenv import load_dotenv


def get_weather_data(**kwargs):
    """retrieve current weather data from openweathermap.org"""

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
        print("Error: no api key supplied")
        return False

    url = "http://api.openweathermap.org/data/2.5/%s?q=%s&appid=%s&units=metric" % (req, city, api_key)
    print(url)

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


def main(file_path, **kwargs):
    load_dotenv()

    weather_api = os.environ.get("WEATHER")

    # get & format data from openweathermaps.org
    data = flatten_dict(get_weather_data(**kwargs))

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

    # check for key-word arguments from bash
    c = 1
    opt_args = {}
    while c < len(sys.argv):
        field = sys.argv[c].strip("-")
        value = sys.argv[c + 1]
        opt_args[field] = value
        c += 2

    if "out_file" in opt_args:
        out_file = opt_args["out_file"]
    else:
        out_file = "openweatherdata_scraped.csv"

    main(out_file, **opt_args)

