import pandas as pd
import pickle
from datetime import datetime
from sklearn.linear_model import LinearRegression

# ignore warnings
import warnings
warnings.filterwarnings('ignore')


def generate_preditction(route, startstop, endstop, date, time, direction):
        # master dictionary of route numbers and their corresponding master files
        master_route_dict = {"18": "Eighteen_Master.csv", "17": "Seventeen_Master.csv", "84A": "EightyFourA_Master.csv",
                             "70D": "SeventyD_Master.csv", "84X": "EightyFourX_Master.csv",
                             "75": "SeventyFive_Master.csv", "84": "EightyFour_Master.csv",
                             "79A": "SeventyNineA_Master.csv", "83A": "EightyThreeA_Master.csv",
                             "79": "SeventyNine_Master.csv", "83": "EightyThree_Master.csv",
                             "77A": "SeventySevenA_Master.csv", "11": "Eleven_Master.csv",
                             "77X": "SeventySevenX_Master.csv", "15A": "FifteenA_Master.csv",
                             "76A": "SeventySixA_Master.csv", "15B": "FifteenB_Master.csv",
                             "76": "SeventySix_Master.csv", "15D": "FifteenD_Master.csv", "70": "Seventy_Master.csv",
                             "15": "Fifteen_Master.csv", "16C": "SixteenC_Master.csv", "54A": "FiftyFourA_Master.csv",
                             "16D": "SixteenD_Master.csv", "16": "Sixteen_Master.csv", "51D": "FiftyOneD_Master.csv",
                             "68A": "SixtyEightA_Master.csv", "51X": "FiftyOneX_Master.csv",
                             "68X": "SixtyEightX_Master.csv", "56A": "FiftySixA_Master.csv",
                             "68": "SixtyEight_Master.csv", "53": "FiftyThree_Master.csv",
                             "65B": "SixtyFiveB_Master.csv", "40B": "FortyB_Master.csv", "65": "SixtyFive_Master.csv",
                             "40D": "FortyD_Master.csv", "69X": "SixtyNineX_Master.csv", "40E": "FortyE_Master.csv",
                             "69": "SixtyNine_Master.csv", "45A": "FortyFiveA_Master.csv", "61": "SixtyOne_Master.csv",
                             "44B": "FortyFourB_Master.csv", "67X": "SixtySevenX_Master.csv",
                             "44": "FortyFour_Master.csv", "67": "SixtySeven_Master.csv", "49": "FortyNine_Master.csv",
                             "66A": "SixtySixA_Master.csv", "41A": "FortyOneA_Master.csv",
                             "66B": "SixtySixB_Master.csv", "41C": "FortyOneC_Master.csv",
                             "66X": "SixtySixX_Master.csv", "41D": "FortyOneD_Master.csv", "66": "SixtySix_Master.csv",
                             "41X": "FortyOneX_Master.csv", "63": "SixtyThree_Master.csv", "41": "FortyOne_Master.csv",
                             "13": "Thirteen_Master.csv", "47": "FortySeven_Master.csv",
                             "38A": "ThirtyEightA_Master.csv", "46A": "FortySixA_Master.csv",
                             "38B": "ThirtyEightB_Master.csv", "46E": "FortySixE_Master.csv",
                             "38D": "ThirtyEightD_Master.csv", "43": "FortyThree_Master.csv",
                             "38": "ThirtyEight_Master.csv", "42D": "FortyTwoD_Master.csv",
                             "39A": "ThirtyNineA_Master.csv", "42": "FortyTwo_Master.csv",
                             "39X": "ThirtyNineX_Master.csv", "40": "Forty_Master.csv", "39": "ThirtyNine_Master.csv",
                             "4": "Four_Master.csv", "31A": "ThirtyOneA_Master.csv", "14C": "FourteenC_Master.csv",
                             "31B": "ThirtyOneB_Master.csv", "14": "Fourteen_Master.csv",
                             "31D": "ThirtyOneD_Master.csv", "31": "ThirtyOne_Master.csv", "9": "Nine_Master.csv",
                             "37": "ThirtySeven_Master.csv", "185": "OneEightyFive_Master.csv",
                             "33A": "ThirtyThreeA_Master.csv", "184": "OneEightyFour_Master.csv",
                             "33B": "ThirtyThreeB_Master.csv", "111": "OneEleven_Master.csv",
                             "33D": "ThirtyThreeD_Master.csv", "151": "OneFiftyOne_Master.csv",
                             "33E": "ThirtyThreeE_Master.csv", "150": "OneFifty_Master.csv",
                             "33": "ThirtyThree_Master.csv", "145": "OneFortyFive_Master.csv",
                             "32X": "ThirtyTwoX_Master.csv", "142": "OneFortyTwo_Master.csv",
                             "32": "ThirtyTwo_Master.csv", "140": "OneForty_Master.csv",
                             "25A": "TwentyFiveA_Master.csv", "114": "OneFourteen_Master.csv",
                             "25B": "TwentyFiveB_Master.csv", "104": "OneOFour_Master.csv",
                             "25D": "TwentyFiveD_Master.csv", "102": "OneOTwo_Master.csv",
                             "25X": "TwentyFiveX_Master.csv", "116": "OneSixteen_Master.csv",
                             "25": "TwentyFive_Master.csv", "161": "OneSixtyOne_Master.csv",
                             "29A": "TwentyNineA_Master.csv", "130": "OneThirty_Master.csv",
                             "27A": "TwentySevenA_Master.csv", "123": "OneTwentyThree_Master.csv",
                             "27B": "TwentySevenB_Master.csv", "122": "OneTwentyTwo_Master.csv",
                             "27X": "TwentySevenX_Master.csv", "120": "OneTwenty_Master.csv",
                             "27": "TwentySeven_Master.csv", "1": "One_Master.csv", "26": "TwentySix_Master.csv",
                             "7A": "SevenA_Master.csv", "270": "TwoSeventy_Master.csv", "7B": "SevenB_Master.csv",
                             "238": "TwoThirtyEight_Master.csv", "7D": "SevenD_Master.csv",
                             "239": "TwoThirtyNine_Master.csv", "7": "Seven_Master.csv",
                             "236": "TwoThirtySix_Master.csv", "17A": "SeventeenA_Master.csv",
                             "220": "TwoTwenty_Master.csv", "59": 'FiftyNine_Master.csv', "41B": 'FortyOneB_Master.csv', '118':'OneEighteen_Master.csv', '33X': 'ThirtyThreeX_Master.csv'}


        #calling the master route file for the given request
        route_file = master_route_dict[str(route)]
        file = "~/Desktop/Master-Route-Files/" + route_file
        df = pd.read_csv(file, keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)

        #dropping some columns we don't need (probably we will remove these from the database but we need to settle on final model first)
        df = df.drop(columns=['TRIPID', 'VEHICLEID', 'LINEID', 'ARRIVALTIME', 'DEPARTURETIME', 'DWELLTIME'])

        #limiting the dataset to only the direction we need
        direction_only = df[df.DIRECTION==int(direction)]

        #getting the main subroute (we will need to make provision for the subroutes)

        subroutes = pd.read_csv("~/Desktop/routes_subroutes-04072020.csv", keep_default_na=True, sep=',\s+', delimiter=',', skipinitialspace=True)
        only_route = subroutes[subroutes.LINEID==route]
        route_direction = only_route[only_route.DIRECTION==int(direction)]
        subroute_list = list(route_direction.MAINROUTE.unique())
        main_subroute = subroute_list[0][2:-2]


        main_route = direction_only[direction_only["ROUTEID"] ==main_subroute]

        #getting the last PROGRNUMBER so that I can...
        progrnumbers = list(main_route.PROGRNUMBER.unique())
        last_progrnumber = max(progrnumbers)

        #getting the datasets for only the first and last stops on the main_route
        only_first = main_route[main_route["STOPPOINTID"]==int(startstop)]
        only_last = main_route[main_route["STOPPOINTID"]==int(endstop)]

        
        #getting the columns I need for merging and changing their name so I can distinguish them
        for_merging = only_last[["PLANNEDTIME_ARR", "ACTUALTIME_ARR", "UNIQUE_TRIP", "DELAYARR", "DELAYDEP"]]
        for_merging.columns = ["PLANNEDTIME_ARR_LAST", "ACTUALTIME_ARR_LAST", "UNIQUE_TRIP", "DELAYARR_LAST", "DELAYDEP_LAST"]

        #Merging
        result = pd.merge(only_first,
                        for_merging[["PLANNEDTIME_ARR_LAST", "ACTUALTIME_ARR_LAST", "UNIQUE_TRIP", "DELAYARR_LAST", "DELAYDEP_LAST"]],
                        on='UNIQUE_TRIP', 
                        how='left')

        #dropping rows with missing values
        reduced_result = result.dropna()


        reduced_result['ACTUALTIME_ARR_LAST'] = reduced_result['ACTUALTIME_ARR_LAST'].astype('int64')
        #creating two new features
        reduced_result['JOURNEYTIME'] = reduced_result["ACTUALTIME_ARR_LAST"] - reduced_result["ACTUALTIME_DEP"]
        reduced_result['PLANNED_JOURNEYTIME'] = reduced_result["PLANNEDTIME_ARR_LAST"] - reduced_result["PLANNEDTIME_DEP"]

        #dropping columns I don't need
        reduced_result = reduced_result.drop(columns=['DAYOFSERVICE','PROGRNUMBER','DELAYDEP', "PLANNED_JOURNEYTIME", 'ROUTEID', 'DELAYARR', 'DIRECTION', 'UNIQUE_TRIP', 'PLANNEDTIME_ARR', 'PLANNEDTIME_DEP', 'ACTUALTIME_ARR', 'ACTUALTIME_DEP', 'PLANNEDTIME_ARR_LAST', 'ACTUALTIME_ARR_LAST', 'DELAYARR_LAST', 'DELAYDEP_LAST', 'STOPPOINTID'])

        #preparing features for linear regression
        df_dummies = pd.get_dummies(reduced_result)

        # y is the target
        y = df_dummies["JOURNEYTIME"]
        # X is everything else
        X = df_dummies.drop(["JOURNEYTIME"],1)


        #running multiple regressions on the data
        multiple_linreg = LinearRegression().fit(X, y)

        #pop my user entered data into a dataframe
        data = {"DAYOFSERVICE":[date], "TIME":[time]}
        test = pd.DataFrame(data)

        #now I need to convert this to MONTH, DAYOFWEEK, TIMEGROUP

        #converting date to date format from string
        date_list = []

        for row in test['DAYOFSERVICE']:
                x = datetime.strptime(row, '%Y-%m-%d')
                date_list.append(x)

        test['DAYOFSERVICE'] = date_list

        #creating month and day of the week feature
        test['MONTH'] = test['DAYOFSERVICE'].dt.month
        test['DAYOFWEEK'] = test['DAYOFSERVICE'].dt.dayofweek


        #Creating Time Group Feature
        time_group_departure = []
        for row in test['TIME']:
                row = int(row)
                if row < 0:
                        print ("Error - negative time stamp")
        
                elif row <= 3600 or (row > 86400 and row <= 90000):
                        time_group_departure.append('0')
                elif row > 3600 and row <= 7200 or (row > 90000 and row <= 93600) :
                        time_group_departure.append('1')
                elif row > 7200 and row <= 10800:
                        time_group_departure.append('2')
                elif row >10800 and row <= 14400:
                        time_group_departure.append('3')
                elif row > 14400 and row <= 18000:
                        time_group_departure.append('4')
                
                elif row > 18000 and row <= 21600:
                        time_group_departure.append('5')
                elif row > 21600 and row <=25200:
                        time_group_departure.append('6')
                elif row > 25200 and row <= 27000:
                        time_group_departure.append('7')
                elif row > 27000 and row <= 28800:
                        time_group_departure.append('8')
                elif row > 28800 and row <= 30600:
                        time_group_departure.append('9')
                
                elif row > 30600 and row <= 32400:
                        time_group_departure.append('10')
                elif row > 32400 and row <= 36000:
                        time_group_departure.append('11')
                elif row > 36000 and row <= 39600:
                        time_group_departure.append('12')
                elif row > 39600 and row <= 43200:
                        time_group_departure.append('13')
                elif row > 43200 and row <= 46800:
                        time_group_departure.append('14')
                
                elif row > 46800 and row <= 50400:
                        time_group_departure.append('15')
                elif row > 50400 and row <= 54000:
                        time_group_departure.append('16')    
                elif row > 54000 and row <= 57600:
                        time_group_departure.append('17')
                elif row > 57600 and row <= 59400:
                        time_group_departure.append('18')
                elif row > 59400 and row <= 61200:
                        time_group_departure.append('19')
        
                elif row > 61200 and row <= 63000:
                        time_group_departure.append('20')
                elif row > 63000 and row <= 64800:
                        time_group_departure.append('21')
                elif row > 64800 and row <= 66600:
                        time_group_departure.append('22')
                elif row > 66600 and row <= 68400:
                        time_group_departure.append('23')
                elif row > 68400 and row <= 72000:
                        time_group_departure.append('24')
        
                elif row > 72000 and row <= 75600:
                        time_group_departure.append('25')
                elif row > 75600 and row <= 79200:
                        time_group_departure.append('26')
                elif row > 79200 and row <= 82800:
                        time_group_departure.append('27')
                elif row > 82800 and row <= 86400:
                        time_group_departure.append('28')


        test['TIME_GROUP'] = time_group_departure

        #drop the date and time features we don't need

        test = test.drop(columns=['DAYOFSERVICE', 'TIME'])

        #get my predictions

        prediction = multiple_linreg.predict(test)

        minutes = int(prediction/60)

        return minutes
