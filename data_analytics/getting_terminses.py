import pandas as pd
import numpy as np
import csv
import os



import warnings
warnings.filterwarnings('ignore')



def how_many_directions(direction1, direction2):
    directions = []
    if no_of_directions == 1:
        
        if no_of_subroutes_direction2 == 0:
            directions.append(1)
        else:
            directions.append(2)
    else:
        directions.append(1)
        directions.append(2)
    return directions
    
        

def get_main_routes(direction):
    main_routes = []
    y = direction['ROUTEID'].value_counts()
    #convert the indices of this dataframe to a list
    z = y.index.values.tolist()
    # list index 0 is the most popular routeID in this direction
    main_routes.append(z[0])
    return main_routes

def get_list_subroute(direction, main_route):
    subs = []
    y = list(direction['ROUTEID'].unique())
    l3 = [x for x in y if x not in main_route]
    subs.append(l3)
    return subs

def stops_main_routes(direction, main_route):
    stops = []
    y = list(direction['ROUTEID'].unique())
    for subroute in y:
        if subroute in main_route:
            p = direction[direction['ROUTEID']==subroute]
            z = list(p['STOPPOINTID'].unique())
            stops.append(z)
    return stops
    

def stops_subroutes (direction, main_route):
    stops = []
    
    y = list(direction['ROUTEID'].unique())
    k = np.setdiff1d(y, main_route)
    for subroute in k:
        p = direction[direction['ROUTEID']==subroute]
        z = list(p['STOPPOINTID'].unique())
        stops.append(z)
    return stops


def perfect_subsets(list1, list2):
    x = []
    for i in range(0, len(list2)):
        x = np.setdiff1d(list2[i], list1)
    if len(x) == 0:
        return True
    else: 
        return False



def firstandlaststopid(main_subroute):
    list_stops = []
    num_progressnos = len(main_subroute['PROGRNUMBER'].unique())
    progressnumbers = list(main_subroute['PROGRNUMBER'].unique())
    
    stoppointid = list(main_subroute['STOPPOINTID'].unique())
   
    first_stop_index = progressnumbers.index(1)

    first_stop = stoppointid[first_stop_index]
    
    list_stops.append(first_stop)
    

    last_stop_index = progressnumbers.index(max(progressnumbers))
    
    last_stop = stoppointid[last_stop_index]
    
    list_stops.append(last_stop)

    return list_stops

def returnroute(direction):
    """returns lineids"""
    
    fee = direction['LINEID'].value_counts()
    #make a list of the LINEIDS
    fi = fee.index.values.tolist()
    #returns the first index of above (ie the most popular one, which will be the LINEID required)
    return fi[0]


#Driver code

count = 0
directory = '/Users/laura/Desktop/Master-Route-Files'
for entry in os.scandir(directory):
    if entry.path.endswith(".csv"):
        print(entry)
        df = pd.read_csv(entry, keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)


        df['DAYOFSERVICE'] = df['DAYOFSERVICE'].astype('datetime64[ns]')
        df['TRIPID'] = df['TRIPID'].astype('category')
        df['PROGRNUMBER'] = df['PROGRNUMBER'].astype('category')
        df['STOPPOINTID'] = df['STOPPOINTID'].astype('category')
        df['LINEID'] = df['LINEID'].astype('category')
        df['DIRECTION'] = df['DIRECTION'].astype('category')
        df['ROUTEID'] = df['ROUTEID'].astype('category')
        df['VEHICLEID'] = df['VEHICLEID'].astype('category')
        df['UNIQUE_TRIP'] = df['UNIQUE_TRIP'].astype('category')
        df['MONTH'] = df['MONTH'].astype('category')
        df['DAYOFWEEK'] = df['DAYOFWEEK'].astype('category')
        df['ARRIVALTIME'] = df['ARRIVALTIME'].astype('<U8')
        df['DEPARTURETIME'] = df['DEPARTURETIME'].astype('<U8')
        df['TIME_GROUP'] = df['TIME_GROUP'].astype('category')

        direction1 = df[df['DIRECTION']==1]
        direction2 = df[df['DIRECTION']==2]


        no_of_directions = df["DIRECTION"].nunique()
        no_of_subroutes_direction1 = direction1["ROUTEID"].nunique()
        no_of_subroutes_direction2 = direction2["ROUTEID"].nunique()

        directions = how_many_directions(direction1, direction2)



        if len(directions) < 1 or len(directions) > 2:
            print ("Error: No. of directions incorrect")

        elif len(directions) == 1 and directions[0] == 1:
            lineid = returnroute(direction1)
            direction = 1
            main_route = get_main_routes(direction1)
            main_route_dataframe = direction1[direction1["ROUTEID"]== main_route[0]]
            subroutes = get_list_subroute(direction1, main_route)
            main_route_stops = stops_main_routes(direction1, main_route)
            subroute_stops = stops_subroutes(direction1, main_route)
            sub_set_of_main = perfect_subsets(main_route_stops, subroute_stops)
            first_last = firstandlaststopid(main_route_dataframe)
            first_stop = first_last[0]
            last_stop = first_last[1]

            with open('b.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    #uncomment below if you need a new header
                    #writer.writerow(["LINEID", "DIRECTION", "MAINROUTE", "SUBROUTES", "SUBROUTES SET OF MAIN", "START_STOP", "END_STOP"])
                    writer.writerow([lineid, direction, main_route, subroutes,  sub_set_of_main,  first_stop, last_stop])
                    count += 1
                    print(count)

        elif len(directions) == 1 and directions[0] == 2:
            lineid = returnroute(direction2)
            direction = 2
            main_route = get_main_routes(direction2)
            main_route_dataframe = direction2[direction2["ROUTEID"]== main_route[0]]
            subroutes = get_list_subroute(direction2, main_route)
            main_route_stops = stops_main_routes(direction2, main_route)
            subroute_stops = stops_subroutes(direction2, main_route)
            sub_set_of_main = perfect_subsets(main_route_stops, subroute_stops)
            first_last = firstandlaststopid(main_route_dataframe)
            first_stop = first_last[0]
            last_stop = first_last[1]

            with open('b.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    #uncomment below if you need a new header
                    #writer.writerow(["LINEID", "DIRECTION", "MAINROUTE", "SUBROUTES", "SUBROUTES SET OF MAIN", "START_STOP", "END_STOP"])
                    writer.writerow([lineid, direction, main_route, subroutes,  sub_set_of_main,  first_stop, last_stop])
                    count += 1
                    print(count)
        else:

            lineid = returnroute(direction1)
            direction = 1
            main_route = get_main_routes(direction1)
            main_route_dataframe = direction1[direction1["ROUTEID"]== main_route[0]]
            subroutes = get_list_subroute(direction1, main_route)
            main_route_stops = stops_main_routes(direction1, main_route)
            subroute_stops = stops_subroutes(direction1, main_route)
            sub_set_of_main = perfect_subsets(main_route_stops[0], subroute_stops)
            first_last = firstandlaststopid(main_route_dataframe)
            first_stop = first_last[0]
            last_stop = first_last[1]

            with open('b.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    #uncomment below if you need a new header
                    #writer.writerow(["LINEID", "DIRECTION", "MAINROUTE", "SUBROUTES", "SUBROUTES SET OF MAIN", "START_STOP", "END_STOP"])
                    writer.writerow([lineid, direction, main_route, subroutes,  sub_set_of_main,  first_stop, last_stop])

            lineid = returnroute(direction2)
            direction = 2
            main_route = get_main_routes(direction2)
            main_route_dataframe = direction2[direction2["ROUTEID"]== main_route[0]]
            subroutes = get_list_subroute(direction2, main_route)
            main_route_stops = stops_main_routes(direction2, main_route)
            subroute_stops = stops_subroutes(direction2, main_route)
            sub_set_of_main = perfect_subsets(main_route_stops, subroute_stops)
            first_last = firstandlaststopid(main_route_dataframe)
            first_stop = first_last[0]
            last_stop = first_last[1]

            with open('b.csv', 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([lineid, direction, main_route, subroutes,  sub_set_of_main,  first_stop, last_stop])
                    count += 1
                    print(count)

#bad_bois = FortyOneB_Master.csv, OneEighteen_Master.csv, ThirtyThreeX_Master.csv

