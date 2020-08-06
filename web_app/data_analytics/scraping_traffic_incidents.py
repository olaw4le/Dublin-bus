import pandas as pd
import csv
import time
import datetime
import numpy as np
import json
import requests
from datetime import datetime
from time import gmtime
from time import strftime
import pg8000 as ps

database = "postgres"
user = "postgres"
password = "YZuB%F34qYSbpp7J"
host = "group-10-dublin-bus.cu4ammu8tjpf.eu-west-1.rds.amazonaws.com"
port = 5432


def construct_sql(**kwargs):

    if "table_name" in kwargs:
        table_name = kwargs["table_name"]
    else:
        print("Error: No table name supplied")
        return False

    if "query_type" in kwargs:
        query_type = kwargs["query_type"]
    else:
        print("Error: No query type supplied")
        return False

    if "column_names" in kwargs:
        cols = ", ".join(kwargs["column_names"])
    else:
        cols = "*"

    # define template structures for sql queries
    templates = {
        "delete_all": "DELETE * FROM %s",
        "select_all": "SELECT * FROM %s",
        "select_where": "SELECT %s FROM %s WHERE %s",
        "insert": "INSERT INTO %s (%s) VALUES (%s)",
        "attr_names": """SELECT column_name FROM information_schema.columns WHERE table_name = '%s' ORDER BY ordinal_position"""
    }

    # if inserting data
    if query_type == "insert":

        # check that data passed as kwarg
        if "data" not in kwargs:
            print("Error: No data supplied for insert query")
            return False

        attr_names = ""
        attr_values = ""

        # for item in data to be inserted;
        # build a string containing the attribute names and attributes values
        for key in kwargs["data"].keys():

            attr_names += "%s, " % key
            val = kwargs["data"][key]

            # place string values in single quotes
            if type(val) not in [int, float]:
                val = "'%s'" % val
            else:
                val = str(val)

            attr_values += "%s, " % val

        # remove ", " from the end of attr_names & attr_Values
        attr_names = attr_names[:-2]
        attr_values = attr_values[:-2]

        # combine the query template, table name, attribute names & attribute values
        sql_query = templates[query_type] % (table_name, attr_names, attr_values)
    
        return sql_query

    # if selecting with predicate
    if query_type == "select_where":

        # check that data passed as kwarg
        if "data" not in kwargs:
            print("Error: No data supplied for insert query")
            return False

        predicates = ""

        # for item in data to be inserted;
        # build a string containing the attribute names and attributes values
        for key in kwargs["data"].keys():

            val = kwargs["data"][key]

            # place string values in single quotes
            if type(val) is str:
                val = "'%s'" % val
            else:
                val = str(val)

            predicates += " %s = %s AND" % (key, val)

        # remove "AND" from the end of attr_names & attr_Values
        predicates = predicates[:-3]

        # combine the query template, table name, attribute names & attribute values
        sql_query = templates[query_type] % (cols, table_name, predicates)
       
        return sql_query

    # if deleting/selecting *all* data from a table
    elif query_type in ["delete_all", "select_all", "attr_names"]:
        sql_query = templates[query_type] % table_name
        
        return sql_query

    else:
        print("Error: Unsupported query type entered")
        return False


def execute_sql(sql_query, database, user, password, host, port, **kwargs):
    
    # is function expected to produce output or not - depends on query type
    if ("retrieving_data" in kwargs) and type(kwargs["retrieving_data"] == bool):
        retrieving_data = kwargs["retrieving_data"]
    else:
        retrieving_data = False

    # try to establish a connection to the database
    try:
        connection = ps.connect(database=database, user=user, password=password, host=host, port=port)
    except Exception as e:
        print("Failed to connect to database")
        print(e)
        return e

    cursor = connection.cursor()

    # try to execute the sql query
    try:
        cursor.execute(sql_query)
        connection.commit()
    except Exception as e:
        connection.close()
        print("Failed to execute sql query")
        print(e)
        return e

    # if retrieving data / expecting some kind of response...
    if retrieving_data:
        
        response = cursor.fetchall()
        
        connection.close()
        return response

    else:
        connection.close()


# api requests - it was necessary to split dublin into four tiles
NW_Dublin = requests.get("https://traffic.ls.hereapi.com/traffic/6.3/incidents/json/10/493/331?apiKey=0J8K2mqx_WBSULDw5RB_JZ74B4MFttAFiR53zZZ3sXk")
Best_Dublin = requests.get("https://traffic.ls.hereapi.com/traffic/6.3/incidents/json/10/494/331?apiKey=0J8K2mqx_WBSULDw5RB_JZ74B4MFttAFiR53zZZ3sXk")
SW_Dublin = requests.get("https://traffic.ls.hereapi.com/traffic/6.3/incidents/json/10/493/332?apiKey=0J8K2mqx_WBSULDw5RB_JZ74B4MFttAFiR53zZZ3sXk")
SE_Dublin = requests.get("https://traffic.ls.hereapi.com/traffic/6.3/incidents/json/10/494/332?apiKey=0J8K2mqx_WBSULDw5RB_JZ74B4MFttAFiR53zZZ3sXk")

# convert to json format
NW_Dublin_JSON = NW_Dublin.json()
Best_Dublin_JSON = Best_Dublin.json()
SW_Dublin_JSON = SW_Dublin.json()
SE_Dublin_JSON = SE_Dublin.json()

# put them in a list
jsons = [NW_Dublin_JSON, Best_Dublin_JSON, SW_Dublin_JSON, SE_Dublin_JSON]

# iterrate the jsons and take the information we require and add it to a list
incidents = []
for JSON in jsons:
    
    if 'TRAFFIC_ITEMS' in JSON.keys():
        items = JSON['TRAFFIC_ITEMS']['TRAFFIC_ITEM']
        
        for item in items:
            id = item['TRAFFIC_ITEM_ID']
            b = item['START_TIME']
            c = item['END_TIME']
            d = item['LOCATION']["GEOLOC"]['ORIGIN']['LATITUDE']
            e = item['LOCATION']["GEOLOC"]['ORIGIN']['LONGITUDE']
            f = item['LOCATION']["GEOLOC"]["TO"][0]['LATITUDE']
            g = item['LOCATION']["GEOLOC"]["TO"][0]['LONGITUDE']
            h = item['TRAFFIC_ITEM_DESCRIPTION'][0]['value']
            from_loc = (d,e)
            to_loc = (f,g)
            try:
                i = item["LOCATION"]["INTERSECTION"]["ORIGIN"]["STREET1"]["ADDRESS1"]
            except:
                i = ""
            path = "%s,%s" % (from_loc, to_loc)
            info = h + " " + i
            incident_info_list = [id, b, c, path, info]
            incidents.append(incident_info_list)
    else:
        continue

# query the database for the shapes of the routes
sql1 = construct_sql(table_name="db_gtfs_shapes", query_type="select_all")
permanent_list = execute_sql(sql1, database, user, password, host, port, retrieving_data=True)

    
new_dict = {}    
for shape in permanent_list:
    paths_of_incidents = []
    bus_path = shape[1]
    for incident in incidents:
        print(shape[0])
        #print(incident[3])
        query = "SELECT path '%s' <-> path '[%s]';" %(bus_path, incident[3])
        
        y = execute_sql(query, database, user, password, host, port, retrieving_data=True)
        distance = y[0][0]
        if float(distance) <= 0.006:
            print(distance)
            paths_of_incidents.append(incident)
    new_dict[shape[0]]=paths_of_incidents

# this sql query will replace the above
"""
"
select route_id
from db_gtfs_shapes
where (route_path <-> path'[%s]') < 0.006;" % incident_path
"""

print(new_dict)