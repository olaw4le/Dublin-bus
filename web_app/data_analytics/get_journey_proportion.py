from data_analytics import db_interface as db
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

    start_index = seq.index(int(start))
    end_index = seq.index(int(end))

    return seq[start_index: end_index + 1]


def segments_from_stops(seq):
    """return list of segments on passed ordered route-stop-sequence"""

    segments = []

    for i, stop in enumerate(seq):
        if i != 0:
            segments.append("s%d_%d" % (seq[i - 1], seq[i]))

    return segments


def get_proportions(route, direction, segments, month, day, time):

    # create sql query
    table_name = "route_%s_%s_proportions" % (str(route), str(direction))
    sql = db.construct_sql(table_name=table_name, query_type="select_where",
                           data={"month": month, "weekday": day, "timegroup": str(time)},
                           column_names=segments)

    # execute sql query
    response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)

    # return the sum of all proportions
    return sum(response[0])


def get_mean_time(route, direction, segments, month, day, time):

    # create sql query
    table_name = "route_%s_%s_means" % (str(route), str(direction))
    sql = db.construct_sql(table_name=table_name, query_type="select_where",
                           data={"month": month, "weekday": day, "timegroup": str(time)},
                           column_names=segments)

    # execute sql query
    response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)

    # return the sum of all proportions
    print(sql)
    print("this is the response")
    print(response)
    return sum(response[0])


def get_standard_dev(route, direction, segments, month, day, time):

    # get the standard deviations
    # create sql query
    table_name = "route_%s_%s_standard_dev" % (str(route), str(direction))
    sql = db.construct_sql(table_name=table_name, query_type="select_where",
                           data={"month": month, "weekday": day, "timegroup": str(time)},
                           column_names=segments)

    # execute sql query
    response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)

    # return the sum of all proportions
    print("this is the response")
    print(response)
    return sum(response[0])


def get_95_percentile(route, direction, segments, month, day, time):
    """calculate the 95th percentile from the means & standard deviations for each segment"""

    means = get_mean_time(route, direction, segments, month, day, time)
    std_dev = get_standard_dev(route, direction, segments, month, day, time)

    return means + (1.645 * std_dev)


"""
# ---- EXAMPLE USAGE ----
all_stops = stops_on_route("145", main=True, direction=1)
print(all_stops)
sub_stops = stops_on_journey(4320, 334, all_stops)
print(sub_stops)
sub_segments = segments_from_stops(sub_stops)
print(sub_segments)
print(get_proportions("145", 1, sub_segments, "January", "Monday", 15))
print(get_95_percentile("145", 1, sub_segments, "January", "Monday", 15))
"""