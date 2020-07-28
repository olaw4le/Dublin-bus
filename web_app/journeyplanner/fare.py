from bs4 import BeautifulSoup
import requests
import json

def get_fare(route, direction, start_stop, end_stop):

    
    fare_details = {}
    fare_details["found"]=False
    direction = int(direction)
    with open("/Users/hannahbarrett/Documents/CompScience/ResearchPracticum/research-project/web_app/journeyplanner/static/journeyplanner/ordered_stops_main.json") as json_file:
        ordered_stops = json.load(json_file)
    route = route.upper()
    fare_details["route"] = route
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
                return fare_details
    else:
        print("No fare")
        return fare_details
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
        # adult_fare = soup.find(id="ctl00_FullRegion_MainRegion_ContentColumns_holder_FareListingControl_lblFare")
        #find the table head that contains the string "all fares"
        head = soup.find_all("th", string=lambda string: string and "All Fares" in string)
        table = head[0].parent.parent
        #loop through rows to find all cells containing "€"
        for row in table.find_all("tr"):
            cells = row.find_all("td")
            if len(cells) == 2 and "€" in str(cells[1].contents[0]):
                #strip the extra whitespace
                print(str(cells[0].contents[0]).strip(), str(cells[1].contents[0]).replace("€", "").strip())
                fare_details[cells[0].contents[0].strip()] = cells[1].contents[0].replace("€", "").strip()

        fare_details["found"]=True
        print(url)
        fare_details["url"] = url
        print("fare details")
        print(fare_details)
        return fare_details
    except:
        return fare_details
    

