import random
from locust import HttpUser, task, between,TaskSet
from django.views.decorators.csrf import csrf_exempt
from django.test import TestCase


# class QuickstartUser(HttpUser):
#     wait_time = between(5, 9)
#
#     # checking if user sent post from the ui works
class PostFunction(HttpUser):
    @classmethod
    def setUpClass(cls):
        super(PostFunction, cls).setUpClass()
    wait_time = between(5, 9)


# function that shows marker for all the stops a route goes through in tab2
    @task
    def find_latlng(self):

        data={'route': ['13'],'stop':['6245']}

        response = self.client.post('/find_latlng/',data)


    @task
# function to find the lat and lng of of a route stop
    def list_latlng(self):
        data={'route': ['13']}
        response = self.client.post('/list_latlng/',data)

# function to show real time in real-time tab
    @task
    def realtime_post(self):
        data= {'stopnumber': ['6245']}
        response = self.client.post('/real_time/',data)


 # view fucntion that shows prediction in tab 2
    @task
    def prediction(self):

        data={'date': ['2020-07-30'], 'time': ['60300'], 'route': ['130'], 'origin': ['1775'], 'destination': ['1778'], 'direction': ['2']}

        response = self.client.post('/prediction/',data)

    @task
    def planner_post(self):
        data= {'data': ['[{"route_number":"14","arrival_stop":"Beaumont Avenue, stop 1046","departure_stop":"Frankfort Avenue, stop 1079","num_stops":10,"departure_latlng":"53.3166603,-6.2707465","arrival_latlng":"53.2933604,-6.2573817","duration":"6"},{"route_number":"17","arrival_stop":"Clonskeagh, Harlech Grove","departure_stop":"Churchtown, Nutgrove Avenue","num_stops":11,"departure_latlng":"53.29419910000001,-6.258802699999999","arrival_latlng":"53.3020144,-6.2279957","duration":"7"}]'], 'date': ['2020-07-28'], 'time': ['81960']}

        response = self.client.post('/planner/',data)







