import os
import json

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
path = cwd


def get_direction_from_stops(route, stop_1, stop_2):
    """Returns a direction (either 1 or 2) when given a route and two stops"""

    # convert the route to uppercase
    route = route.upper()
   
    # get our json file with the ordered list of stops on each route.
    stops_file = "%s/journeyplanner/static/journeyplanner/ordered_stops_main.json" % path
    with open(stops_file) as f:
        stops_dict = json.load(f)
        route = str(route).upper()

    # iterate through the dictionary to find the main subroute for the route, and if the 
    for key, value in stops_dict[route].items():
        if stops_dict[route][key]['main'] is True:
            if int(stop_1) in stops_dict[route][key]['stops'] and int(stop_2) in stops_dict[route][key]['stops']:
                return stops_dict[route][key]['direction']
    else:
        raise EnvironmentError
