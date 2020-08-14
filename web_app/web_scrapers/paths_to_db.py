# from data_analytics import db_interface as db
from db_interface.db_interface import *
import csv

# hard code env variables to appease laura - major security vulnerability !
database = "postgres"
user = "postgres"
password = "YZuB%F34qYSbpp7J"
host = "group-10-dublin-bus.cu4ammu8tjpf.eu-west-1.rds.amazonaws.com"
port = 5432

file_path = "route_shapes.csv"

with open(file_path, "r") as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:

        sql = construct_sql(table_name="db_gtfs_shapes", query_type="insert", data=dict(row))
        print(sql)

        # execute sql query
        print(execute_sql(sql, database, user, password, host, port))

