import requests
import json
import datetime
import time
# all bus due time at a bus stop
url1 = 'https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=2007&format=json'

# due time for a specific bus
url2 = 'https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid=6245&routeid=151&format=json'

all_bus = requests.get(url1)
one_bus = requests.get(url2)

result1 = all_bus.json()
result2 = one_bus.json()

print(result1)
print(result2)
print("\n")


print("Stop number " +result1['stopid'] )
for item in result1['results']:
 print("Bus " + item['route'] + " is due in " + item['duetime'] + " minutes")
