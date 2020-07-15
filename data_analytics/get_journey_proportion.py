import db_interface as db
import json
import os
from dotenv import load_dotenv

load_dotenv()
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")

# 1. find segments in journey
# 2. query database for segment proportions
# 3. return sum of proportions

# from routeID, sub-route - return sequence of stop numbers on route
sequence = ()


def stops_on_route(route, main=False, direction=1):
    """query the database return a sequence of all stops on a given sub-route"""

    # create sql query
    if main:
        sql = db.construct_sql(table_name="routes", query_type="select_where", data={"ID": route})
    else:
        sql = db.construct_sql(table_name="routes", query_type="select_where", data={"ID": route.split("_")[0]})

    # execute sql query
    response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)
    print(response)

    if main:
        # return the 'main' sub-route in the passed direction
        for sub_route in response[0][1].keys():
            if response[0][1][sub_route]["main"] and (response[0][1][sub_route]["direction"] == direction):
                return response[0][1][sub_route]["stops"]
    else:
        return response[0][1][route]["stops"]


def stops_on_journey(start, end, seq):
    """return all stops on a given route-sequence between a
        start and end start (including the start & end stop)"""

    start_index = seq.index(start)
    end_index = seq.index(end)

    return seq[start_index, end_index + 1]


def segments_from_stops(seq):
    """return list of segments on passed ordered route-stop-sequence"""

    segments = []

    for i, stop in enumerate(seq):
        if i != 0:
            segments.append("s%d-%d" % (seq[i - 1], seq[i]))

    return segments


def get_proportions(route, direction, segments, month, day, time):

    sql = "SELECT %s FROM %s WHERE Month = %d AND Weekday = %d AND TimeGroup = %d"
    table_name = "route_%s_%s_proportions" % (str(route), str(direction))
    attrs = ""
    for s in segments:
        attrs += "%s + "
    attrs = attrs[:-2]
    sql = sql % (table_name, attrs, month, day, time)

    # execute sql query
    response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)

    return response


print(stops_on_route(270, main=True, direction=1))
#print(get_proportions(270, 2, segments_from_stops(stops_on_journey(3352, 3337, stops_on_route(270, main=True, direction=1))), 2, 2, 15))
