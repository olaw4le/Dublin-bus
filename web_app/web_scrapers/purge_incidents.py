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


def purge_incidents():
    # get incident id's & end times for all incidents in the database
    sql = "SELECT incident_id, end_time FROM incident_data"
    response = db.execute_sql(sql, database, user, password, host, port, retrieving_data=True)

    # remove incident data relating to incidents in the past
    now = datetime.now()
    for incident in response:
        if incident[1] < now:
            # remove this incident from the incident lookup table
            sql = "DELETE FROM incident_lookup WHERE incident_id = '%s'" % incident[0]
            db.execute_sql(sql, database, user, password, host, port, retrieving_data=False)
            # remove this incident from the incident data table
            sql = "DELETE FROM incident_data WHERE incident_id = '%s'" % incident[0]
            db.execute_sql(sql, database, user, password, host, port, retrieving_data=False)


if __name__ is "__main__":
    purge_incidents()
