from vincenty import vincenty
import json
import os

path = os.getcwd()
# /Users/olawalebmg/research-project/web_app/journeyplanner/static/routes/7.json


# function to find the coordinates of the stops a route goes through
def stops_latlng(route_number):
    route_file = "%s/journeyplanner/static/routes/%s.json" % (path, route_number)

    stops_coordinate = {}

    with open(route_file, encoding='utf-8') as f:
        data = json.loads(f.read())

    for i in data["results"]:
        for j in i["stops"]:
            lat = float(j["latitude"])
            lng = float(j["longitude"])
            stop_id = j["stopid"]
            stops_coordinate[stop_id] = {"lat": lat, "lng": lng}

    return stops_coordinate


# function to find the stop number when given the lat and lng
def find_stop(stop_list, lat_lng):
    for key in stop_list.keys():
        # Calculate the geographical distance between 2 points using the vincenty formula and updating the list
        stop_list[key].update(
            {"distance": vincenty([stop_list[key]["lat"], stop_list[key]["lng"]], lat_lng)})

    # Sort the dictionary by the shortest distance
    sorted_list = sorted(stop_list.items(), key=lambda x_y: x_y[1]["distance"])

    # Return the closest stop id to the given lat_lng
    stop = sorted_list[0][0]
    return stop


# finding the lat and lng of a stop
def latlng(stop_list, stop):
    result = stop_list[stop]
    
    return result


