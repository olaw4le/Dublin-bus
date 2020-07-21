import pandas as pd
import ntpath
import sys


def merge_from_csv(bus_file, weather_file, **kwargs):
    """merges two passed .csv files and either returns a pandas
    Dataframe object or writes the merged data to a new .csv file"""

    if "write_to_file" in kwargs:
        write_to_file = kwargs["write_to_file"]
    else:
        write_to_file = "false"
    print (bus_file)
    print (weather_file)
    print (kwargs)
    # import data for the bus route
    route_data = pd.read_csv(bus_file)
    print(route_data.head())
    # import data for weather
    weather_data = pd.read_csv(weather_file)
    print(weather_data.head())
    # create a "date" feature to "route_data" to allow merging with "weather_data" on feature "date"

    # container for the new feature data
    date_list = []

    # populate container feature by associating "DAYOFSERVICE" and
    # "ACTUALTIME_ARR" with the nearest hourly weather entry
    for index, row in route_data.iterrows():

        date = row["DAYOFSERVICE"]
        time = row["ACTUALTIME_ARR"]
        dt = pd.Timestamp(date) + pd.to_timedelta(time, unit="s")

        # round timestamp to the nearest hour
        dt = dt.replace(second=0, microsecond=0, minute=0) + pd.to_timedelta(dt.minute // 30, unit="h")

        # assign dt as value of route_data.date
        date_list.append(dt)

    # add a "date" feature to "route_data" to allow merging with "weather_data"
    route_data["date"] = date_list
    print("date feature added to bus list")
    # ensure that weather_data "date" feature is of type datetime64
    weather_data["date"] = pd.to_datetime(weather_data["date"])

    # merge the two data frames on feature "date"
    combined_data = pd.merge(weather_data, route_data, on="date")
    print("combined")
    if write_to_file == "false":
        return combined_data
    else:

        # get / create the name for the output file
        if "outfile" in kwargs:
            outfile = kwargs["outfile"]
        else:
            outfile = "%s_bus_weather_combined.csv" % (ntpath.basename(bus_file).split("_")[0])

        # save merged data
        combined_data.to_csv(outfile, index=False)


if __name__ == "__main__":

    bus = sys.argv[1]
    weather = sys.argv[2]

    # check for key-word arguments from bash
    c = 3
    opt_args = {}
    while c < len(sys.argv):
        field = sys.argv[c].strip("-")
        print(field)
        value = sys.argv[c+1]
        print(value)
        opt_args[field] = value
        c += 2

    merge_from_csv(bus, weather, **opt_args)

