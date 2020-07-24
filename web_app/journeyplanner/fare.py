from bs4 import BeautifulSoup
import requests
import json

def get_fare(route, direction, start_stop, end_stop):


        
    with open("/Users/hannahbarrett/Documents/CompScience/ResearchPracticum/research-project/web_app/journeyplanner/static/journeyplanner/ordered_stops_main.json") as json_file:
        ordered_stops = json.load(json_file)
    route_dict = ordered_stops[route]
    for subroute in route_dict:
        if route_dict[subroute]["main"] and route_dict[subroute]["direction"] == direction:
            start_stop_idx = route_dict[subroute]["stops"].index(start_stop)
            end_stop_idx = route_dict[subroute]["stops"].index(end_stop)

    if direction == 2:
        direction = "O"
    elif direction == 1:
        direction = "I"
    else:
        return None
    url = f"https://www.dublinbus.ie/Fare-Calculator/Fare-Calculator-Results/?routeNumber={route}&direction={direction}&board={start_stop_idx}&alight={end_stop_idx}"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    fare = soup.find(id="ctl00_FullRegion_MainRegion_ContentColumns_holder_FareListingControl_lblFare")
    return fare.contents[0]

print(get_fare("4",1,7113,408))

