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


with open("ordered_stops_main.json") as file:

    # convert json data to dict
    data = json.load(file)

    # for each route
    for route in data.keys():

        # create a dictionary with the route ID and a string representation of the JSON data...
        db_entry = {"ID": route, "info": json.dumps(data[route])}

        # build an sql query to insert json data to db
        sql = db.construct_sql(table_name="routes", query_type="insert", data=db_entry)

        # execute the sql query
        print(db.execute_sql(sql, database, user, password, host, port))
