from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(10,20)
    
    @task 
    def routeplanner(self):
        self.client.get("/routeplanner/")
        self.client.get("/static/journeyplanner/routeplanner.js")
        
    @task
    def allroutes(self):
        self.client.get("/allroutes/")
        self.client.get("/static/journeyplanner/estimator.js")
    

    @task
    def realtime(self):
        self.client.get("/realtime/")
        self.client.get("/static/journeyplanner/realtime.js")

    @task
    def tourist(self):
        self.client.get("/tourist/")
        self.client.get("/static/journeyplanner/touristmap.js")

    @task
    def leapcard(self):
        self.client.get("/leap/")
        self.client.get("/static/journeyplanner/leapcard.js")
