from bs4 import BeautifulSoup
import requests
import json

def get_fare(route, direction, start_stop, end_stop):


    direction = int(direction)
    with open("/Users/hannahbarrett/Documents/CompScience/ResearchPracticum/research-project/web_app/journeyplanner/static/journeyplanner/ordered_stops_main.json") as json_file:
        ordered_stops = json.load(json_file)
    route_dict = ordered_stops[route]
    print("looking for", direction)
    for subroute in route_dict:
        print(route_dict[subroute]["direction"])
        print(route_dict[subroute]["main"])
        if route_dict[subroute]["main"] and int(route_dict[subroute]["direction"]) == int(direction):
            try:
                start_stop_idx = route_dict[subroute]["stops"].index(int(start_stop))
                end_stop_idx = route_dict[subroute]["stops"].index(int(end_stop))
                break
            except: 
                return None
    else:
        print("No fare soz")
        return None
    if direction == 2:
        direction = "I"
    elif direction == 1:
        direction = "O"
    else:
        return None
    url = f"https://www.dublinbus.ie/Fare-Calculator/Fare-Calculator-Results/?routeNumber={route}&direction={direction}&board={start_stop_idx}&alight={end_stop_idx}"
    page = requests.get(url)
    try: 
        soup = BeautifulSoup(page.text, 'html.parser')
        fare = soup.find(id="ctl00_FullRegion_MainRegion_ContentColumns_holder_FareListingControl_lblFare")
        print(url)
        return fare.contents[0]
    except:
        return None

# print(get_fare("4",1,7113,408))

