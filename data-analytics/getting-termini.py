import pandas as pd
import numpy as np
import csv
import os



import warnings
warnings.filterwarnings('ignore')


def getmainroutes(direction1, direction2):
    """returns a list of the main routes"""
    
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


def returnroute(direction1, direction2):
    """returns a list of the line ids - expected to be the same for both directions"""
    directions = [direction1, direction2]
    line_id = []
    #iterate through the list of directions
    for direction in directions: 
        #get a series of only the lineIDS and their counts  
        fee = direction['LINEID'].value_counts()
        #make a list of the LINEIDS
        fi = fee.index.values.tolist()
        #returns the first index of above (ie the most popular one, which will be the LINEID required)
        line_id.append(fi[0])
    return line_id


def perfectsubset(direction1, direction2, main_routes):
    """returns True if the less popular ROUTEIDs are perfect subsets of the main route. Otherwise returns False"""
    directions = [direction1, direction2]

    for direction in directions:
        z = []
        y = direction['ROUTEID'].value_counts()
        
        if len(y) > 1:
            z = int(len(y)/2)

        for row in y:
            if row != 0:
                t = list(y[y != 0].index[0:z])

        
        not_main = []
        
        for i in t:
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


#def driver_code(a):
    #"""driver code and writes to .csv file"""
count = 0
directory = '/Users/laura/Desktop/Master-Route-Files'
for entry in os.scandir(directory):
    if entry.path.endswith(".csv"):
        df = pd.read_csv(entry, keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)

#df = pd.read_csv("/Users/laura/Desktop/FortyFour_Master.csv", keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
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
            
        lineid = returnroute(direction1, direction2)
        print(lineid)

        mainroutes = getmainroutes(direction1, direction2)

        main_dir1 = direction1[direction1['ROUTEID']==mainroutes[0]]
        main_dir2 = direction2[direction2['ROUTEID']==mainroutes[1]]


        y = perfectsubset(direction1, direction2, mainroutes)

        v = firstandlaststopid(main_dir1)
        w = firstandlaststopid(main_dir2)
            

        with open('start_end_stops.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            #uncomment below if you need a new header
            #writer.writerow(["LINEID", "MAINROUTE", "PERFECT_SUBROUTE", "DIRECTION", "START_STOP", "END_STOP"])
            writer.writerow([lineid[0], mainroutes[0], y, 1, v[0], v[1]])
            writer.writerow([lineid[1], mainroutes[1], y, 2, w[0], w[1]])
            print(count)
            count += 1
        
#if __name__ == "__main__":
    #a = sys.argv[1]

    #driver_code(a)

