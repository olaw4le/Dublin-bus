from web_app.journeyplanner.route_details import stops_latlng, find_stop,latlng

def test_stops_latlng():
   #testing wether the stops lat and lng for a given route isnt empty
    routelist = stops_latlng(1)
    assert routelist != None



def test_find_stop():
    #testing the vicenty formular that returns the stop number 
    routelist= stops_latlng("76A")
    lat_lng=(53.3879611111,-6.3792833333)
    test= find_stop(routelist, lat_lng)
    assert test== "1840"


def test_latlng():
    #testing if the lat and lng for a given stop is returned
    routelist = stops_latlng("46A")
    test= latlng(routelist,"812")
    assert test !=  None




test_latlng()
