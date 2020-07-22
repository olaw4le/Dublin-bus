import requests
import json


def get_bus_data(route_number):
    pass

def get_route_stops(route_number, **kwargs):

    if "operator" in kwargs:
        operator = kwargs["operator"]
    else:
        operator = "bac"

    if "format" in kwargs:
        resp_format = kwargs["format"]
    else:
        resp_format = "json"

    url = "https://data.smartdublin.ie/cgi-bin/rtpi/routeinformation?routeid=%s&operator=%s&format=%s" % (route_number,
                                                                                                          operator,
                                                                                                          resp_format)

    # get route info and convert to python dict
    response = requests.get(url)
    results = json.loads(response.text)["results"]

    stops = []
    for i in results:
        print(i)
        #stops.append(i["stopid"])

    return stops


print(get_route_stops(41))
