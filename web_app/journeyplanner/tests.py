from django.test import TestCase
from django.shortcuts import reverse
from django.test import Client
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select


# Create your tests here.
csrf_client = Client(enforce_csrf_checks=True)


class Testviews(TestCase):
    # testing the allroutes page url
    def test_allroutes(self):
        response=self.client.get("/allroutes/")
        self.assertEquals(response.status_code, 200)
    
    # checking the if the right template was used for the allroutes page
    def test_allroutes_templates(self):
        response=self.client.get(reverse("allroutes"))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response, "journeyplanner/allroutes.html")

    # realtime page url
    def test_realtime(self):
        response = self.client.get("/realtime/")
        self.assertEquals(response.status_code,200)
    
    # real time page templates
    def test_realtime_templates(self):
        response = self.client.get(reverse("realtime"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "journeyplanner/realtime.html")

    # routeplanner page url
    def test_routeplanner(self):
        response = self.client.get("/routeplanner/")
        self.assertEquals(response.status_code, 200)
    
    # routeplanner page templates
    def test_routeplanner_templates(self):
        response = self.client.get(reverse("routeplanner"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "journeyplanner/routeplanner.html")

    # tourist page url
    def test_tourist(self):
        response = self.client.get("/tourist/")
        self.assertEquals(response.status_code, 200)
    
    # tourist page templates
    def test_tourist_templates(self):
        response = self.client.get(reverse("tourist"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "journeyplanner/tourist.html")

    # leap page url
    def test_leap(self):
        response = self.client.get("/leap/")
        self.assertEquals(response.status_code, 200)
    
  # tourist page templates
    def test_leap_templates(self):
        response=self.client.get(reverse("leap"))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "journeyplanner/leap.html")


# checking if user sent post from the ui works 
class PostFunction(TestCase):
    @classmethod
    def setUpClass(cls):
        super(PostFunction, cls).setUpClass()

    # function that shows marker for all the stops a route goes through in tab2
    def find_latlng(self):
        self.client = Client()

        data = {'route': ['13'], 'stop': ['6245']}

        response = self.client.post('/find_latlng/', data)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

# function to find the lat and lng of of a route stop 
    def list_latlng(self):
        self.client = Client()
        data={'route': ['13']}
        response = self.client.post('/list_latlng/', data)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    # function to show real time in real-time tab
    def realtime_post(self):
        self.client = Client()

        data= {'stopnumber': ['6245']}

        response = self.client.post('/real_time/', data)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    # view function that shows prediction in tab 2
    def prediction(self):
        self.client = Client()

        data = {
            'date': ['2020-07-30'],
            'time': ['60300'],
            'route': ['130'],
            'origin': ['1775'],
            'destination': ['1778'],
            'direction': ['2']
        }

        response = self.client.post('/prediction/',data)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def planner_post(self):
        self.client = Client()
        data = {
            'data':
                ['[{"route_number":"14","arrival_stop":"Beaumont Avenue, stop 1046","departure_stop":"Frankfort Avenue, stop 1079","num_stops":10,"departure_latlng":"53.3166603,-6.2707465","arrival_latlng":"53.2933604,-6.2573817","duration":"6"},{"route_number":"17","arrival_stop":"Clonskeagh, Harlech Grove","departure_stop":"Churchtown, Nutgrove Avenue","num_stops":11,"departure_latlng":"53.29419910000001,-6.258802699999999","arrival_latlng":"53.3020144,-6.2279957","duration":"7"}]'],
            'date': ['2020-07-28'],
            'time': ['81960']
        }

        response = self.client.post('/planner/', data)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

