import db_interface as db
import get_current_weather as get
from datetime import datetime
import os
import sys
import pytz
from dotenv import load_dotenv


def update_db_weather(database, user, password, host, port, api_key, req, **kwargs):

    if "city" in kwargs:
        city = kwargs["city"]
    else:
        city = "Dublin,,372"            # 372 is the ISO 3166 Country Code for Ireland

    def insert_data(weather_data, table_name):

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
        sql_query = db.construct_sql(query_type="insert", table_name=table_name, data=data)
        print(db.execute_sql(sql_query, database=database, user=user, password=password, host=host, port=port,
                             retrieveing_data=False))

    # retrieve weather data
    raw_weather_data = get.get_weather_data(req_type=req, city=city, key=api_key)

    # if retrieving bulk forecast data...
    if req == "forecast":

        # delete existing data on this table...
        sql = db.construct_sql(query_type="delete_all", table_name="weather_data_forecast")
        db.execute_sql(sql, database=database, user=user, password=password, host=host, port=port,
                       retrieveing_data=False)

        # insert new data into table row-by-row
        for row in raw_weather_data["list"]:
            insert_data(get.flatten_dict(row), "weather_data_forecast")

    else:
        # delete existing data on this table...
        sql = db.construct_sql(query_type="delete_all", table_name="weather_data_current")
        db.execute_sql(sql, database=database, user=user, password=password, host=host, port=port,
                       retrieveing_data=False)

        # insert new data row to table
        insert_data(get.flatten_dict(raw_weather_data), "weather_data_current")


if __name__ == "__main__":

    # load environment variables
    load_dotenv()

    args = {
        "database": os.getenv("database"),
        "user": os.getenv("user"),
        "password": os.getenv("password"),
        "host": os.getenv("host"),
        "port": os.getenv("port"),
        "api_key": os.getenv("weather_api_key"),
        "request": "current"
    }

    # read the request type (ie. whether to get current of forecast data) from the cli
    if len(sys.argv) > 1:
        args["request"] = sys.argv[1]

    # run the main method
    print(update_db_weather(args["database"], args["user"], args["password"], args["host"],
                            args["port"], args["api_key"], args["request"]))
