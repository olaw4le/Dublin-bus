from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
    @task 
    def routeplanner(self):
        self.client.get("/routeplanner/")
        self.client.get("/static/journeyplanner/routeplanner.js")
        data= {'data': ['[{"route_number":"14","arrival_stop":"Beaumont Avenue, stop 1046","departure_stop":"Frankfort Avenue, stop 1079","num_stops":10,"departure_latlng":"53.3166603,-6.2707465","arrival_latlng":"53.2933604,-6.2573817","duration":"6"},{"route_number":"17","arrival_stop":"Clonskeagh, Harlech Grove","departure_stop":"Churchtown, Nutgrove Avenue","num_stops":11,"departure_latlng":"53.29419910000001,-6.258802699999999","arrival_latlng":"53.3020144,-6.2279957","duration":"7"}]'], 'date': ['2020-07-28'], 'time': ['81960']}
        self.client.post('/planner/',data)
        
    @task
    def allroutes(self):
        self.client.get("/allroutes/")
        self.client.get("/static/journeyplanner/estimator.js")
        data={'date': ['2020-07-30'], 'time': ['60300'], 'route': ['130'], 'origin': ['1775'], 'destination': ['1778'], 'direction': ['2']}
        self.client.post('/prediction/',data)

    @task
    def realtime(self):
        self.client.get("/realtime/")
        self.client.get("/static/journeyplanner/realtime.js")
        data= {'stopnumber': ['6245']}
        self.client.post('/real_time/',data)

    @task
    def tourist(self):
        self.client.get("/tourist/")
        self.client.get("/static/journeyplanner/touristmap.js")

        
    @task
    def leapcard(self):
        self.client.get("/leap/")
        self.client.get("/static/journeyplanner/leapcard.js")






    
