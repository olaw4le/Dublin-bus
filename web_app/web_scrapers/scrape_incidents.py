from web_app.db_interface import db_interface as db
from dotenv import load_dotenv, find_dotenv
import os
import requests
from datetime import datetime

# locate & read .env file
load_dotenv(find_dotenv())

database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
host = os.getenv("host")
port = os.getenv("port")
traffic_key = os.getenv("traffic_key")

api_url = "https://traffic.ls.hereapi.com/traffic/6.3/incidents/json/10/%s?apiKey=%s"

# api grid refs - needed 4 to cover all of dublin
grid_refs = {
    "NW_Dublin": "493/331",
    "NE_Dublin": "494/331",
    "SW_Dublin": "493/332",
    "SE_Dublin": "494/332"
}

# retrieve incident data & assemble in list
incidents = []

for ref in grid_refs:
    url = api_url % (grid_refs[ref], traffic_key)
    incidents_json = requests.get(url).json()

    try:
        traffic_items = incidents_json['TRAFFIC_ITEMS']['TRAFFIC_ITEM']

    except Exception as e:
        print(e)
        continue

    for item in traffic_items:
        incident = {
            "incident_id": item['TRAFFIC_ITEM_ID'],
            "start_time": item['START_TIME'],
            "end_time": item['END_TIME'],
            "start_point": (item['LOCATION']["GEOLOC"]['ORIGIN']['LATITUDE'],
                            item['LOCATION']["GEOLOC"]['ORIGIN']['LONGITUDE']),
            "end_point": (item['LOCATION']["GEOLOC"]["TO"][0]['LATITUDE'],
                          item['LOCATION']["GEOLOC"]["TO"][0]['LONGITUDE']),
            "incident_path": "",
            "desc_line_1": item['TRAFFIC_ITEM_DESCRIPTION'][0]['value'],
            "decs_line_2": ""
        }

        try:
            incident["decs_line_2"] = item["LOCATION"]["INTERSECTION"]["ORIGIN"]["STREET1"]["ADDRESS1"]
        except Exception as e:
            print(e)

        incident["incident_path"] = "[%s, %s]" % (incident["start_point"], incident["end_point"])

        incidents.append(incident)


# iterate through incidents and work out if they are relevant - if so store on database

# sql query for checking if incident is within ~500m of a bus route
path_sql = """
    select route_id 
    from db_gtfs_shapes
    where (route_path <-> path'%s') < 0.006;
    """

now = datetime.now()

for incident in incidents:

    # skip incidents that are already over
    dt = datetime.strptime(incident["end_time"], "%m/%d/%Y %H:%M:%S")
    if now > dt:
        continue

    # check if this incident intersects with any bus route
    sql = path_sql % incident["incident_path"]

    # return a list of bus routes that are effected by this disruption
    response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)

    if len(response) > 0:

        # populate the lookup table
        for route in response:

            entry = {"incident_id": incident["incident_id"], "route_id": route[0]}
            sql = db.construct_sql(table_name="incident_lookup", query_type="insert", data=entry)

            # execute sql query
            response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=False)

        # add this incident as an entry into the incident_data table
        sql = db.construct_sql(table_name="incident_data", query_type="insert", data=incident)
        response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=False)
