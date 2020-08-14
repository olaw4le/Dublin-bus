from bs4 import BeautifulSoup
import requests
import json
from pathlib import Path

base_path = Path(__file__).parent
file_path = (base_path / "static/journeyplanner/ordered_stops_main.json").resolve()


def get_fare(route, direction, start_stop, end_stop):
    """function which takes a route, direction, start and end stops and scrapes the dublin bus
    website to obtain the fare"""

    # initialise fare dictionary and set flag to false
    fare_details = dict()
    fare_details["found"] = False

    # get stops for specific route from JSON
    with open(file_path) as json_file:
        ordered_stops = json.load(json_file)
    route = route.upper()
    fare_details["route"] = route
    try:
        route_dict = ordered_stops[route]
    except Exception as e:
        print(e)
        return fare_details
    if direction:
        direction = int(direction)
    else:
        return fare_details
    # get index of start and stop routes from main subroute in the JSON
    for sub_route in route_dict:
        if route_dict[sub_route]["main"] and int(route_dict[sub_route]["direction"]) == int(direction):
            try:
                start_stop_idx = route_dict[sub_route]["stops"].index(int(start_stop))
                end_stop_idx = route_dict[sub_route]["stops"].index(int(end_stop))
                break
            except Exception as e:
                print(e)
                return fare_details
    else:
        return fare_details

    # convert direction to required format for Dublin Bus website
    if direction == 2:
        direction = "I"
    elif direction == 1:
        direction = "O"
    else:
        return fare_details
    url = f"https://www.dublinbus.ie/Fare-Calculator/Fare-Calculator-Results/?routeNumber={route.lower()}&direction={direction}&board={start_stop_idx}&alight={end_stop_idx}"
    fare_details["url"] = url
    try: 
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        # find the table head that contains the string "all fares"
        head = soup.find_all("th", string=lambda string: string and "All Fares" in string)
        table = head[0].parent.parent
        # loop through rows to find all cells containing "€"
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) == 2 and "€" in str(cells[1].contents[0]):
                # strip the extra whitespace
                print(str(cells[0].contents[0]).strip(), str(cells[1].contents[0]).replace("€", "").strip())
                fare_details[cells[0].contents[0].strip()] = cells[1].contents[0].replace("€", "").strip()

        # change flag to true if found
        fare_details["found"] = True
        fare_details["url"] = url
        return fare_details

    except Exception as e:
        print(e)
        return fare_details
    

