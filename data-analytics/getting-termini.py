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

#separating dataframe into directions
direction1 = df[df['DIRECTION']==1]
direction2 = df[df['DIRECTION']==2]

#list of the two directions
directions = [direction1, direction2]

#itterate throught list of directions
for direction in directions:
    #get the most popular route ID in this direction

    #get a dataframe with the most popular ROUTEID first
    y = direction['ROUTEID'].value_counts()
    #convert the indices of this dataframe to a list
    z = y.index.values.tolist()
    # list index 0 is the most popular routeID in this direction
    print("One of the main routes is: ", z[0])

    main= z[0]



    
