
import os


cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory


path = cwd#[:-7] #UNCOMMENT THE [:-7] IF RUNNING FROM WITHIN DJANGO ++++++=====++++++====+++



def get_direction_from_stops(route, stop_1, stop_2):
    import json
    stops_file = f"{path}/web_app/journeyplanner/static/journeyplanner/ordered_stops_main.json"
    with open(stops_file) as f:
        stops_dict = json.load(f)
    for subroute in stops_dict[route]:
        stops = stops_dict[route][subroute]["stops"]
        if stop_1 in stops:
            idx_1 = stops.index(stop_1)
            if stop_2 in stops[idx_1:]:
                return stops_dict[route][subroute]["direction"]
        else:
            continue   


if __name__ == "__main__":
    route = "65"
    stop_1 = 7208
    stop_2 = 4054 

    # Returns 2     
    print(get_direction_from_stops(route, stop_1, stop_2))

    route = "66A"
    stop_1 = 494
    stop_2 = 2219 

    # Returns 1    
    print(get_direction_from_stops(route, stop_1, stop_2))