import random
from locust import HttpUser, task, between
from django.views.decorators.csrf import csrf_exempt

class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def find_latlng(self):

        response = self.client.get("/routeplanner/")
        csrftoken = response.cookies['csrftoken']

        data={'date': ['2020-07-30'], 'time': ['60300'], 'route': ['130'], 'origin': ['1775'], 'destination': ['1778'], 'direction': ['2']}
        
        response = self.client.post('/routeplanner/', data,headers={"X-CSRFToken": csrftoken},
                     cookies={"csrftoken": csrftoken})


    @task
    def list_latlng(self):
        
        response = self.client.get("/realtime/")
        csrftoken = response.cookies['csrftoken']

        data= {'stopnumber': ['6245']}

        response = self.client.post('/realtime/',data,headers={"X-CSRFToken": csrftoken},
                     cookies={"csrftoken": csrftoken})




# function to show real time in real-time tab
#     @task
#     def realtime_post(self):
#         self.client = Client()

#         data= {'stopnumber': ['6245']}

#         response = self.client.post('/real_time/',data)

#        # Check that the response is 200 OK.
#         self.assertEqual(response.status_code, 200)
        
         
#  # view fucntion that shows prediction in tab 2
#     @task
#     def prediction(self):
#         self.client = Client()

#         data={'date': ['2020-07-30'], 'time': ['60300'], 'route': ['130'], 'origin': ['1775'], 'destination': ['1778'], 'direction': ['2']}

#         response = self.client.post('/prediction/',data)

#        # Check that the response is 200 OK.
#         self.assertEqual(response.status_code, 200)


#     @task
#     def planner_post(self):
#         self.client = Client()
#         data= {'data': ['[{"route_number":"14","arrival_stop":"Beaumont Avenue, stop 1046","departure_stop":"Frankfort Avenue, stop 1079","num_stops":10,"departure_latlng":"53.3166603,-6.2707465","arrival_latlng":"53.2933604,-6.2573817","duration":"6"},{"route_number":"17","arrival_stop":"Clonskeagh, Harlech Grove","departure_stop":"Churchtown, Nutgrove Avenue","num_stops":11,"departure_latlng":"53.29419910000001,-6.258802699999999","arrival_latlng":"53.3020144,-6.2279957","duration":"7"}]'], 'date': ['2020-07-28'], 'time': ['81960']}

#         response = self.client.post('/planner/',data)

#        # Check that the response is 200 OK.
#         self.assertEqual(response.status_code, 200)



