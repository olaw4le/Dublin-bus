import os

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory

path = cwd


def get_direction_from_stops(route, stop_1, stop_2):
    route = route.upper()
    print("in get direction")
    print(route, stop_1, stop_2)
    import json
    stops_file = "%s/journeyplanner/static/journeyplanner/ordered_stops_main.json" % path
    with open(stops_file) as f:
        stops_dict = json.load(f)
        route = str(route).upper()

    for key, value in stops_dict[route].items():
        
        if stops_dict[route][key]['main'] is True:
            if int(stop_1) in stops_dict[route][key]['stops']:
                print("found stop on list!")
                return stops_dict[route][key]['direction']
    else:
        return EnvironmentError
