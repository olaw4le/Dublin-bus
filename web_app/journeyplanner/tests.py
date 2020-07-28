from django.test import TestCase,client 
from django.shortcuts import reverse
from django.test import Client


# Create your tests here.

class Testviews(TestCase):
    ##testing the allroutes page url
    def test_allroutes(self):
        response=self.client.get("/allroutes/")
        self.assertEquals(response.status_code,200)
    
    ##checking the if the right template was used for the allroutes page 
    def test_allroutes_templates(self):
        response=self.client.get(reverse("allroutes"))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"journeyplanner/allroutes.html")

    ## realtime page url 
    def test_realtime(self):
        response=self.client.get("/realtime/")
        self.assertEquals(response.status_code,200)
    
    ## real time page templates
    def test_realtime_templates(self):
        response=self.client.get(reverse("realtime"))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"journeyplanner/realtime.html")

    ## routeplanner page url 
    def test_routeplanner(self):
        response=self.client.get("/routeplanner/")
        self.assertEquals(response.status_code,200)
    
     ## routeplanner page templates
    def test_routeplanner_templates(self):
        response=self.client.get(reverse("routeplanner"))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"journeyplanner/routeplanner.html")

     ## tourist page url 
    def test_tourist(self):
        response=self.client.get("/tourist/")
        self.assertEquals(response.status_code,200)
    
     ## tourist page templates
    def test_tourist_templates(self):
        response=self.client.get(reverse("tourist"))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"journeyplanner/tourist.html")

    ## leap page url 
    def test_leap(self):
        response=self.client.get("/leap/")
        self.assertEquals(response.status_code,200)
    
  ## tourist page templates
    def test_leap_templates(self):
        response=self.client.get(reverse("leap"))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"journeyplanner/leap.html")




# class routeplannerTest(TestCase):
#     @classmethod
#     def tearDownClass(cls):
#         pass

#     def setUpClass(self):
#         self.client = Client()

#     def test_addAccount(self):
#         data= {'data': ['[{"route_number":"14","arrival_stop":"Beaumont Avenue, stop 1046","departure_stop":"Frankfort Avenue, stop 1079","num_stops":10,"departure_latlng":"53.3166603,-6.2707465","arrival_latlng":"53.2933604,-6.2573817","duration":"6"},{"route_number":"17","arrival_stop":"Clonskeagh, Harlech Grove","departure_stop":"Churchtown, Nutgrove Avenue","num_stops":11,"departure_latlng":"53.29419910000001,-6.258802699999999","arrival_latlng":"53.3020144,-6.2279957","duration":"7"}]'], 'date': ['2020-07-28'], 'time': ['81960']}

#         response = self.client.post('/routeplanner/',data)

#        # Check that the response is 200 OK.
#         self.assertEqual(response.status_code, 200)



class RealtimeTest(TestCase):

    def setUpClass(self):
        self.client = Client()

    def test_addAccount(self):

        response = self.client.post('/routeplanner/',6245)

       # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    


