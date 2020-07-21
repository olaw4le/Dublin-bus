from django.test import TestCase,client 
from django.shortcuts import reverse
from tastypie.test import ResourceTestCase

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











