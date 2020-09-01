# from data_analytics import db_interface as db
from db_interface.db_interface import *
import csv
import os
from dotenv import find_dotenv, load_dotenv

# get environment variables
load_dotenv(find_dotenv())
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")

file_path = "route_shapes.csv"

with open(file_path, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:

        sql = construct_sql(table_name="db_gtfs_shapes", query_type="insert", data=dict(row))
        print(sql)

        # execute sql query
        print(execute_sql(sql, database, user, password, host, port))

