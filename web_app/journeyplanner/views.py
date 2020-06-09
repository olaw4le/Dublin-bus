from django.shortcuts import render
from django.http import HttpResponse

# create home function to handle traffic from journeyplanner app
# return what we want the user to see when they are sent to this route

# request arg has to be here
def home(request):
    return HttpResponse('<h1>HomePage!</h1>')

def about(request):
    return HttpResponse('<h1>About Page!</h1>')

# Create your views here.

