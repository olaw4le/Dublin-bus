from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse
import sys
sys.path.append("..")
from data_analytics import linear_regression


#showing how data can be added to a html page
posts = [
    {
        'route':'Route 9',
        'from' :'Charlestown',
        'to':'Limekiln Avenue',
        'time':'10:40'
    },
    {
        'route':'Route 39',
        'from' :'Burlington Road',
        'to':'Ongar',
        'time':'07:00'
    }
]



# create home function to handle traffic from journeyplanner app
# return what we want the user to see when they are sent to this route

# request arg has to be here
def home(request):
    #context is a dictionary. the keys will be accessible from within the home.html template
    context = {
        'posts': posts
    }
    # context is given as argument. This passes that data into the home template
    # posts variable will now be accessible from within home.html
    return render(request, 'journeyplanner/home.html', context) #render still returns a HttpResponse

def about(request):
    # can also pass dictionary in directly as arg
    return render(request, 'journeyplanner/about.html', {'title': 'About'})

# Create your views here.

def routeplanner(request):
    # can also pass dictionary in directly as arg
    return render(request, 'journeyplanner/routeplanner.html')

def allroutes(request):
    # can also pass dictionary in directly as arg
    return render(request, 'journeyplanner/allroutes.html')

def leap(request):
    # can also pass dictionary in directly as arg
    return render(request, 'journeyplanner/leap.html')

def disruptions(request):
    # can also pass dictionary in directly as arg
    return render(request, 'journeyplanner/disruptions.html')

def tourist(request):
    # can also pass dictionary in directly as arg
    return render(request, 'journeyplanner/tourist.html')


@csrf_exempt
def prediction(request):
    if request.method == "POST":
        route= request.POST["route"]
        origin= request.POST["origin"]
        destination = request.POST["destination"]
        date = request.POST["date"]
        time = request.POST["time"]
        direction=request.POST["direction"]
        print("time from views.py", time)

        result = linear_regression.generate_preditction(route, origin, destination, date, time, direction)
        


        print("routes:",route)
        print("origin:",origin)
        print("destination:",destination)
        print("direction:",direction)
        print("date",date)
        # print("result", result)
    return HttpResponse(result)

@csrf_exempt
def planner(request):
    if request.method == "POST":
        data= request.POST["bus_details"]
        return HttpResponse("")


