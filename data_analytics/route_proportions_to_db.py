import db_interface as db
import get_journey_proportion as gt
import json
import os
from dotenv import load_dotenv

load_dotenv()
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")


def create_table(table_name, segment_names):

    # sql query template
    sql = """CREATE TABLE %s (Month VARCHAR NOT NULL, Weekday VARCHAR NOT NULL, TimeGroup VARCHAR NOT NULL,%s PRIMARY KEY(Month, Weekday, TimeGroup));"""

    # create a string of all segment names & data types
    attr = ""
    for s in segment_names:
        attr += " s%s DOUBLE PRECISION," % s.replace("-", "_")

    # populate sql template
    sql = sql % (table_name, attr)

    # execute the sql query
    print(db.execute_sql(sql, database, user, password, host, port))


def get_segment_names(route):

    # retrieve a list with all stops on this route
    stops = gt.stops_on_route(route.split("_")[0], True, int(route.split("_")[1]))

    # create the segment names
    segments = gt.segments_from_stops(stops)

    return segments


def proportions_to_db(route):

    # read data
    fp = "%s_proportions.json" % route
    with open(fp) as file:
        # convert json data to dict
        data = json.load(file)

    # get list of segment names in data
    segment_names = get_segment_names(route)

    # create table
    table_name = "route_%s_proportions" % route
    create_table(table_name, segment_names)

    # for row in data add an entry to this table if there is data to add, otherwise skip....
    for key in data.keys():
        if "proportions" in data[key].keys():
            entry = data[key]["proportions"]

            # prefix all segment names with asn 'S' to avoid numeric leading character in attr names
            old_keys = list(entry.keys())
            for k in old_keys:
                entry["s%s" % k] = entry.pop(k)

            key_as_list = key.split("_")
            entry["Month"] = key_as_list[1]
            entry["Weekday"] = key_as_list[0]
            entry["TimeGroup"] = key_as_list[2]

            # build sql query
            sql = db.construct_sql(table_name=table_name, query_type="insert", data=entry)

            # execute sql query
            print(db.execute_sql(sql, database, user, password, host, port))


if __name__ is "__main__":
    proportions_to_db("270_2")


