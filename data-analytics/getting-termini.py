import pandas as pd
import numpy as np

import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv("~/Desktop/Trimester_3/FortyFour_Master.csv", keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)

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


def getmainroutes(direction1, direction2):
    """returns a list of the main routes"""
    #separating dataframe into directions
    

    #list of the two directions
    directions = [direction1, direction2]
    main_routes = []
    #itterate throught list of directions
    for direction in directions:
    #get the most popular route ID in this direction

        #get a dataframe with the most popular ROUTEID first
        y = direction['ROUTEID'].value_counts()
        #convert the indices of this dataframe to a list
        z = y.index.values.tolist()
        
        # list index 0 is the most popular routeID in this direction
        main_routes.append(z[0])
    return main_routes

def perfectsubset(direction1, direction2, main_routes):
    directions = [direction1, direction2]

    for direction in directions:
        z = []
        y = direction['ROUTEID'].value_counts()
        
        z = int(len(y)/2)
        for row in y:
            if row != 0:
                v = list(y[y != 0].index[0:z])

        
        not_main = []
        
        for i in v:
            if i in main_routes:
                main_id = i
            else: 
                not_main.append(i)
        
        main = direction[direction['ROUTEID']== main_id]
        stops_on_main = list(main['STOPPOINTID'].unique())

        for i in not_main:
            subroute = direction[direction['ROUTEID']==i]
            stops_on_subroute = list(subroute['STOPPOINTID'].unique())
            if len(list(np.setdiff1d(stops_on_subroute, stops_on_main))) == 0:
                continue
            else:
                return False
    return True


def firstandlaststopid(direction):
    list_stops = []
    num_progressnos = len(direction['PROGRNUMBER'].unique())
    progressnumbers = list(direction['PROGRNUMBER'].unique())
    
    stoppointid = list(direction['STOPPOINTID'].unique())
   
    first_stop_index = progressnumbers.index(1)

    first_stop = stoppointid[first_stop_index]
    
    list_stops.append(first_stop)
    

    last_stop_index = progressnumbers.index(num_progressnos)
    
    last_stop = stoppointid[last_stop_index]
    
    list_stops.append(last_stop)

    return list_stops


mainroutes = getmainroutes(direction1, direction2)
main_dir1 = direction1[direction1['ROUTEID']==mainroutes[0]]
main_dir2 = direction2[direction2['ROUTEID']==mainroutes[1]]

y = perfectsubset(direction1, direction2, mainroutes)
if y:
    print("all subroutes are perfect subsets")
else:
    print("some subroutes are not perfect subsets")

v = firstandlaststopid(main_dir1)
w = firstandlaststopid(main_dir2)
combo = list(v + w)
print (list(set(combo)))