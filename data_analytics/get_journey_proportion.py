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


def stops_on_route(route):
    """query the database return a sequence of all stops on a given sub-route"""

    # create sql query
    sql = db.construct_sql(table_name="routes", query_type="select_where", data={"ID": route.split("_")[0]})

    # execute sql query
    response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)
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
            segments.append("%d-%d" % (seq[i - 1], seq[i]))

    return segments


