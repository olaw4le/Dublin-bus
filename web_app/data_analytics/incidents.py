# from data_analytics import db_interface as db
import db_interface.db_interface as db


# load environment
database = "postgres"
user = "postgres"
password = "YZuB%F34qYSbpp7J"
host = "group-10-dublin-bus.cu4ammu8tjpf.eu-west-1.rds.amazonaws.com"
port = 5432

def return_incident_info(route, direction, date, time, start_stop_x, start_stop_y, end_stop_x, end_stop_y):
    print(route)
    print(direction)
    print(date)
    print(time)
    route_string = str(route.lower()) + "_" + str(direction)
    print(route_string)
    sql = "SELECT * FROM incident_lookup l, incident_data d WHERE l.route_id = %s AND l.incident_id = d.incident_id;" % (route_string)
    x = db.execute_sql(sql, database, user, password, host, port)
    
    return [(start_stop_x, start_stop_y), (end_stop_x, end_stop_y), 'Closed between Balbutcher Lane and R108 - Closed. ']