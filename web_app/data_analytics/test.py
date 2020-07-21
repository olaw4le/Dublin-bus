import db_interface as db

# load environment
database = "postgres"
user = "postgres"
password = "YZuB%F34qYSbpp7J"
host = "group-10-dublin-bus.cu4ammu8tjpf.eu-west-1.rds.amazonaws.com"
port = 5432
weather_api_key = "86baa129046e5cbaeb16af074356e579"

route = 31
direction = 1

month = "January"
weekday = "Monday"
time_group = 27

""" code for line 192 """
route_name = str(route) + "_" + str(direction)

# construct sql query
sql = db.construct_sql(table_name="model_features", query_type="select_where",
                       column_names=["features"], data={"id": route_name})

# execute sql query
response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)[0][0]

""" code for line 355 """
# construct sql query
table_name = "route_%s_%s_proportions" % (route, direction)
sql = db.construct_sql(table_name=table_name, query_type="select_where",
                       data={"month": month, "weekday": weekday, "timegroup": str(time_group)})

# execute sql query
response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)[0]
