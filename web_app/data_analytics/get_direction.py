import os


cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory


path = cwd[:-7] #UNCOMMENT THE [:-7] IF RUNNING FROM WITHIN DJANGO ++++++=====++++++====+++



def get_direction_from_stops(route, stop_1, stop_2):
    import json
    stops_file = f"{path}/web_app/journeyplanner/static/journeyplanner/ordered_stops_main.json"
    with open(stops_file) as f:
        stops_dict = json.load(f)
        route = str(route).upper()

    for key, value in stops_dict[route].items():
        
        if stops_dict[route][key]['main'] == True:
            if int(stop_1) in stops_dict[route][key]['stops']:
                print("found stop on list!")
                return(stops_dict[route][key]['direction']) 
            else:
                return EnvironmentError