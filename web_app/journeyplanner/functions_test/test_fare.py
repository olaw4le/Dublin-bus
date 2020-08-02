from web_app.journeyplanner.fare import *

# this function should pass because the file exist

# this assertion should not throw an error because the file exist

def test_fare():
    testing= get_fare('14', '1', '1079', '1046')
    assert len(testing) != None




test_fare()


