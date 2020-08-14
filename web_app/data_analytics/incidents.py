# from data_analytics import db_interface as db
import db_interface.db_interface as db
from datetime import datetime
from vincenty import vincenty

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
    
    sql = "SELECT * FROM incident_lookup l, incident_data d WHERE l.route_id = '%s' AND l.incident_id = d.incident_id;" % (route_string)
    
    datetime_request = date + "_"+ time
    try:
        date_time_obj = datetime.strptime(datetime_request, '%y-%m-%d %H:%M')
        print(date_time_obj)
    except:
        print("no datetime")

    X = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)
    results_list = []
    #print("X = ", x)
    for item in X:
        #print(item[1])
        sublist = []
        if "Abbey Cottages" not in item[8] and "and Ormond Street" not in item[7]:
            sql1 = "SELECT * FROM db_gtfs_shapes WHERE route_id = '%s';" % (route_string)
            shapes = db.execute_sql(sql1, database, user, password, host, port, retrieving_data=True)
            
            point_1 = (start_stop_x, start_stop_y)
            point_2 = (end_stop_x, end_stop_y)
            
            q = (shapes[0][1]).split("),(")
            new_list = []
            distance_list_origin = []
            distance_list_destination = []
            for item_q in q:
                if ')]' in item_q:
                    item_1 = item_q.replace(')]', '')
                    item_2 = item_1.replace("'", "")
                elif '[(' in item_q:
                    item_1 = item_q.replace('[(', '')
                    item_2 = item_1.replace("'", "")
                else:
                    item_2 = item_q.replace("'", "")
                    new_list.append(item_2)

            for q in new_list:
                r = q.split(',')
                x = float(r[0])
                y = float(r[1])

                point_on_route = (x, y)
                    
                u = vincenty(point_1, point_on_route)
                distance_list_origin.append(u)
                v = vincenty(point_2, point_on_route)
                distance_list_destination.append(v)

            #print(distance_list_origin)
            #print(distance_list_destination)
            nearest_match_origin = min(distance_list_origin)
            nearest_match_destination = min(distance_list_destination)

            #print(nearest_match_origin, nearest_match_destination)
            start_cut = distance_list_origin.index(nearest_match_origin)
            #print("Start cut", start_cut)

            end_cut = distance_list_destination.index(nearest_match_destination)
            #print("End cut", end_cut)

            users_route = new_list[start_cut:end_cut]

            #make users_route into a path for postgresql
            postgre_path = "'["
            for item_6 in users_route:
                item_2 = item_6.replace("'", "")
                #print(item_2)
                postgre_path += "(%s),"%(item_2)
            
            postgre_path += "]'"
            final_postgrepath = postgre_path[:-3] + postgre_path[-2:]
            #print(final_postgrepath)

            incident_path = "[%s,%s]"  %(item[5], item[6])
        
            #print (incident_path)

            sql2 = "SELECT path '%s' <-> path %s;" %(incident_path, final_postgrepath)
            #print (sql2)
            distance_user_route = db.execute_sql(sql2, database, user, password, host, port, retrieving_data=True)

            if (distance_user_route[0][0]) <= 0.006:
                
                response_string = str(item[7]) + " " + str(item[8])
                results_list.append(response_string)
            

    return [results_list]