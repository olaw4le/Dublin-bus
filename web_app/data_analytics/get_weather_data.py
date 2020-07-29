# logic for determining which weather data to pass to the prediciton models
from data_analytics import db_interface as db
from datetime import datetime
import json
import os
from dotenv import load_dotenv

"""
load_dotenv()
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
"""

# hard code env variables to appease laura - major security vulnerability !
database = "postgres"
user = "postgres"
password = "YZuB%F34qYSbpp7J"
host = "group-10-dublin-bus.cu4ammu8tjpf.eu-west-1.rds.amazonaws.com"
port = 5432


# 1. check if date is within forecast -- this info could be kept on the web server to speed up queries??
# 2. If so query the database for the nearest forecast
# 3. otherwise default to the current weather ??


def get_nearest_forecast(date_obj):
    # sql statement for selecting the weather forecast closest to the passed date

    if type(date_obj) is datetime:
        # extract a string format time from the date
        date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S.f")
    elif type(date_obj) is str:
        # assume the passed string is in the correct format - some error checking should really go here
        date_str = date_obj
    else:
        print("Error: must pass DateTime object or string in the format 'yyyy-mm-dd hh:mm:ss.ms'")
        return Exception

    # sql template - populate with date string in format 'yyyy-mm-dd hh:mm:ss.ms'
    sql = """SELECT *
    FROM weather_data_forecast
    ORDER BY ABS(date::DATE - '%s'::DATE)
    LIMIT 1;""" % date_str

    try:
        # execute sql query
        response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)
        return response

    except Exception as e:
        print(e)
        return e


# example use of function get_nearest_forecast()
"""
dt = DateTime("2020-07-31 12:00:00")
print(get_nearest_forecast(dt))
print(get_nearest_forecast("1990-11-23 12:00:00.0000"))
"""
