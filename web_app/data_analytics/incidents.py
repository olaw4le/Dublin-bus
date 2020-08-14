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

    """will return a list containing strings of descriptive information, each pertaining to a single traffic incident. Returns an """
 
    # get the route and direction string to use to query the database
    route_string = str(route.lower()) + "_" + str(direction)
    
    # query the database
    sql = "SELECT * FROM incident_lookup l, incident_data d WHERE l.route_id = '%s' AND l.incident_id = d.incident_id;" % (route_string)
    relevant_incidents = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)

    #create a list to hold the results
    results_list = []
    
    #itterate through the list of traffic incidents relevant to this route
    for incident in relevant_incidents:
        
        # the api really isn't great, so I just decided to remove these two incidents from the lists because Abbey
        # Cottages was showing for every bus that passes through the city centre, but its a tiny back lane off Abbey Street.
        # and the ormand street one was a duplicate with a different ID code. 

        if "Abbey Cottages" not in incident[8] and "and Ormond Street" not in incident[7]:
            
            #get the shape of the bus route from the database
            sql1 = "SELECT * FROM db_gtfs_shapes WHERE route_id = '%s';" % (route_string)
            route_shape = db.execute_sql(sql1, database, user, password, host, port, retrieving_data=True)
            
            # create points from the user's origin and destination lat and long
            origin_bus_stop_location = (start_stop_x, start_stop_y)
            destination_bus_stop_location = (end_stop_x, end_stop_y)
            
            # declare lists for the points on the shape, and the distance from each of those points to the
            # origin and destination stop
            list_of_points_on_shape = []
            distance_list_origin = []
            distance_list_destination = []

            # extract the actual points from the path string
            points_on_shape = (route_shape[0][1]).split("),(")
            for point in points_on_shape:
                if ')]' in point:
                    temp1 = point.replace(')]', '')
                    temp2 = temp1.replace("'", "")
                    list_of_points_on_shape.append(temp2)
                elif '[(' in point:
                    temp1 = point.replace('[(', '')
                    temp2 = temp1.replace("'", "")
                    list_of_points_on_shape.append(temp2)
                else:
                    temp2 = point.replace("'", "")
                    list_of_points_on_shape.append(temp2)

            # find out how far every point on the shape is from the origin and destination stops
            for item in list_of_points_on_shape:
                coordinates_list = item.split(',')
                lat = float(coordinates_list[0])
                lon = float(coordinates_list[1])

                point_on_route = (lat, lon)
                    
                distance_from_origin_stop_to_points_on_shape = vincenty(origin_bus_stop_location, point_on_route)
                distance_list_origin.append(distance_from_origin_stop_to_points_on_shape)
                distance_from_dest_stop_to_points_on_shape = vincenty(destination_bus_stop_location, point_on_route)
                distance_list_destination.append(distance_from_dest_stop_to_points_on_shape)
  
            # finding the closest point to the origin stop on the route shape
            nearest_match_origin = min(distance_list_origin)

            # finding the closest point to the destination stop on the route shape
            nearest_match_destination = min(distance_list_destination)

            # the index of the nearest match to the origin on the list of route shapes
            start_cut = distance_list_origin.index(nearest_match_origin)

            # the index of the nearest match to the destination on the list of route shapes
            end_cut = distance_list_destination.index(nearest_match_destination)

            # segment of the route that the user travels
            users_route = new_list[start_cut:end_cut]

            # make users_route into a path for postgresql
            postgre_path = "'["
            for item_6 in users_route:
                item_2 = item_6.replace("'", "")
                postgre_path += "(%s),"%(item_2)
            
            postgre_path += "]'"
            final_postgrepath = postgre_path[:-3] + postgre_path[-2:]

            # make the incident start and stop points into a path
            incident_path = "[%s,%s]"  %(incident[5], incident[6])

            # query the database for the 'distance' between points
            sql2 = "SELECT path '%s' <-> path %s;" %(incident_path, final_postgrepath)
            distance_user_route = db.execute_sql(sql2, database, user, password, host, port, retrieving_data=True)

            # 0.006 is around about 400m 
            # append the descriptive info to the response string
            if (distance_user_route[0][0]) <= 0.006:
                response_string = str(incident[7]) + " " + str(incident[8])
                results_list.append(response_string)
            
    # randomly decide to put your list inside anther list because you're exhausted and don't know what you're doing
    # and then be unable to remove it because now the front end expects it this way.
    return [results_list]