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



# checking if user sent post from the ui works 
class PostFunction(TestCase):
    @classmethod
    def setUpClass(cls):
        super(PostFunction, cls).setUpClass()


# function that shows marker for all the stops a route goes through in tab2
    def find_latlng(self):
        self.client = Client()

        data={'route': ['13'],'stop':['6245']}

        response = self.client.post('/find_latlng/',data)

         # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

# function to find the lat and lng of of a route stop 
    def list_latlng(self):
        self.client = Client()
        data={'route': ['13']}
        response = self.client.post('/list_latlng/',data)

         # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

# function to show real time in real-time tab

    def realtime_post(self):
        self.client = Client()

        data= {'stopnumber': ['6245']}

        response = self.client.post('/real_time/',data)

       # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)
        
         
 # view fucntion that shows prediction in tab 2
    def prediction(self):
        self.client = Client()

        data={'date': ['2020-07-30'], 'time': ['60300'], 'route': ['130'], 'origin': ['1775'], 'destination': ['1778'], 'direction': ['2']}

        response = self.client.post('/prediction/',data)

       # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def planner_post(self):
        self.client = Client()
        data= {'data': ['[{"route_number":"14","arrival_stop":"Beaumont Avenue, stop 1046","departure_stop":"Frankfort Avenue, stop 1079","num_stops":10,"departure_latlng":"53.3166603,-6.2707465","arrival_latlng":"53.2933604,-6.2573817","duration":"6"},{"route_number":"17","arrival_stop":"Clonskeagh, Harlech Grove","departure_stop":"Churchtown, Nutgrove Avenue","num_stops":11,"departure_latlng":"53.29419910000001,-6.258802699999999","arrival_latlng":"53.3020144,-6.2279957","duration":"7"}]'], 'date': ['2020-07-28'], 'time': ['81960']}

        response = self.client.post('/planner/',data)

       # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


# using selenium webdriver
class webdriver_test(StaticLiveServerTestCase):
   
    @classmethod
    def setUpClass(cls):
        super(webdriver_test, cls).setUpClass()
        cls.selenium = webdriver.Chrome(ChromeDriverManager().install())
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(webdriver_test, cls).tearDownClass()

    # in the realtime tab put 123 in the search box
    def realtime(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/realtime/'))
        user_input = self.selenium.find_element_by_id("Stop-number")
        user_input.send_keys(123)

    # in the leap card tab input the these login details
    def leapcard(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/leap/'))
        user_email = self.selenium.find_element_by_id("leap-user")
        user_email.send_keys('admin@outlook.com')

        user_password =self.selenium.find_element_by_id("leap-password")
        user_password.send_keys("admin")

    # routeplenner tab 
    def routeplanner(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/routeplanner/'))
        user_origin = self.selenium.find_element_by_id("origin")
        user_origin.send_keys('UCD Sports Centre, Belfield, Dublin, Ireland')
        
        user_destination= self.selenium.find_element_by_id("destination")
        user_destination.send_keys('Ballsbridge, Dublin, Ireland')

        user_date= self.selenium.find_element_by_id("destination")
        user_date.send_keys('25/09/2020, 20:20')

    def allroute(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/allroutes/'))
        user_input = self.selenium.find_element_by_id("estimator-route")
        user_input.send_keys('151 towards Bargy Road')
        
        user_origin= self.selenium.find_element_by_id("destination")
        user_origin.select_by_visible_text('4606 Balgaddy Road')

        user_destination= self.selenium.find_element_by_id("destination")
        user_destination.select_by_visible_text('7142 Foxborough Rise')


    def tourist(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/tourist/'))
        user_origin = self.selenium.find_element_by_id("origin-tourist")
        user_origin.send_keys('67 Eccles Street, Northside, Dublin, Ireland')
        







        