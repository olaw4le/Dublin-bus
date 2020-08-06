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

#api requests and convert to JSON 

NW_Dublin = requests.get("https://traffic.ls.hereapi.com/traffic/6.3/incidents/json/10/493/331?apiKey=0J8K2mqx_WBSULDw5RB_JZ74B4MFttAFiR53zZZ3sXk")
Best_Dublin = requests.get("https://traffic.ls.hereapi.com/traffic/6.3/incidents/json/10/494/331?apiKey=0J8K2mqx_WBSULDw5RB_JZ74B4MFttAFiR53zZZ3sXk")
SW_Dublin = requests.get("https://traffic.ls.hereapi.com/traffic/6.3/incidents/json/10/493/332?apiKey=0J8K2mqx_WBSULDw5RB_JZ74B4MFttAFiR53zZZ3sXk")
SE_Dublin = requests.get("https://traffic.ls.hereapi.com/traffic/6.3/incidents/json/10/494/332?apiKey=0J8K2mqx_WBSULDw5RB_JZ74B4MFttAFiR53zZZ3sXk")


NW_Dublin_JSON = NW_Dublin.json()
Best_Dublin_JSON = Best_Dublin.json()
SW_Dublin_JSON = SW_Dublin.json()
SE_Dublin_JSON = SE_Dublin.json()

jsons = [NW_Dublin_JSON, Best_Dublin_JSON, SW_Dublin_JSON, SE_Dublin_JSON]

with open('sample_incident_data_filtered.csv', 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Start_Time", "End_Time", "From", "To", "Desc_1", "Desc_2"])

for JSON in jsons:
    #print(JSON)
    if 'TRAFFIC_ITEMS' in JSON.keys():
        items = JSON['TRAFFIC_ITEMS']['TRAFFIC_ITEM']
        for item in items:
            a = item['TRAFFIC_ITEM_ID']
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
            with open('sample_incident_data_filtered.csv', 'a', newline='') as file:
                writer = csv.writer(file, delimiter =';')
                writer.writerow([a, b, c, tuple(from_loc), tuple(to_loc), h, i])
    else:
        continue