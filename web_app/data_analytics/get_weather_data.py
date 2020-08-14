import db_interface.db_interface as db
from datetime import datetime


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
        date_str = date_obj.strftime("%Y-%m-%d %H:%M:%S.%f")
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


def time_from_seconds(seconds):
    """ takes an int representing the number of seconds since midnight
    & return a 24hr string representation of that time"""

    try:
        seconds = int(seconds)
    except Exception as e:
        print("Error: unable to cast str '%s' as int" % seconds)
        return e

    # guard statement - return "00:00:00" if seconds == to 1 day
    if seconds == 86400:
        return "00:00:00"

    # guard statement - if passed a number greater than total seconds in day use
    # the modulo of the passed seconds and total seconds in a day
    if seconds > 86400:
        # make recursive to reuse the initial guard statement ~ ¯\_(ツ)_/¯ I'm lazy
        return time_from_seconds(seconds % 86400)

    # calculate the int vales for hours/minutes/seconds, cast as type string and pad with 0's
    hours = str(seconds // 3600).zfill(2)
    remainder = seconds % 3600
    minutes = str(remainder // 60).zfill(2)
    seconds = str(remainder % 60).zfill(2)

    return "%s:%s:%s" % (hours, minutes, seconds)


# example use of function get_nearest_forecast()
"""
dt = DateTime("2020-07-31 12:00:00")
print(get_nearest_forecast(dt))
print(get_nearest_forecast("1990-11-23 12:00:00.0000"))
"""
