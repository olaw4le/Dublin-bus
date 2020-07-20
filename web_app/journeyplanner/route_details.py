from vincenty import vincenty
import json

#function to find the coordinates of the stops a route goes through
def stops_latlng(route_number):
    routefile = "web_app/journeyplanner/static/routes/{}.json".format(route_number)

    stops_coordinate = {}

    with open(routefile, encoding='utf-8') as f:
        data = json.loads(f.read())

    for i in data["results"]:
        for j in i["stops"]:
            lat = float(j["latitude"])
            lng = float(j["longitude"])
            stop_id = j["stopid"]
            stops_coordinate[stop_id] = {"lat": lat, "lng": lng}

    return stops_coordinate

#function to find the stop number when given the lat and lng 
def find_stop(stopList, lat_lng):
    for key in stopList.keys():
        # Calculate the geographical distanc between 2 points using the vincenty formular and updating the list
        stopList[key].update(
            {"distance": vincenty([stopList[key]["lat"], stopList[key]["lng"]], lat_lng)})

    # Sort the dictionary by the shortest distance
    sortedList = sorted(stopList.items(), key=lambda x_y: x_y[1]["distance"])

    # Return the closest stop id to the given lat_lng
    stop = sortedList[0][0]
    return stop


# finding the lat and lng of a stop
def latlng(stopList,stop):
    result=stopList[stop]
    
    return result


