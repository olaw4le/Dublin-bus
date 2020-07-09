from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse
import sys
sys.path.append("..")
from data_analytics import linear_regression
from .route_details import stops_latlng, find_stop,latlng
import json


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
        data= json.loads(request.POST["data"])

        prediction=[] #list to store the calculated predictions
      
        buses =len(data)
        for i in range(0,buses):
           route= data[i]["route_number"]
           date = request.POST["date"]
           time = request.POST["time"]
           direction=1

           #departure stops lat and lng
           departure=data[i]["departure_latlng"]
           x=departure.split(",")
           departure_lat = float(x[0])
           departure_lng = float(x[1])

           #arrival stops lat and lng 
           arrival=data[i]["arrival_latlng"]
           x=arrival.split(",")
           arrival_lat = float(x[0])
           arrival_lng = float(x[1])
        

           route_number=route.upper()
           # getting the suggested route file 
           route_list=stops_latlng(route_number)

           #getting the orging and destination stop number using the vincenty formular 
           origin=find_stop(route_list,(departure_lat,departure_lng))
           arrival=find_stop(route_list,(arrival_lat,arrival_lng))

        #    #use the maachine learning module to calculate prediction 
           calculation=linear_regression.generate_preditction(route, origin, arrival, date, time, diection)

        #    #adding the calculated value to the list that will be sent back
           prediction.append(calculation)


           print("origin",date)
           print("Arrival",time)

    print(prediction)

       
        
    return HttpResponse("")
    

@csrf_exempt
def find_latlng(request):
    if request.method == "POST":
        route = request.POST["route"]
        stop_id = request.POST["stop"]
        route_number=route.upper()

        # getting the suggested route file 
        route_list=stops_latlng(route_number)
        result =latlng(route_list,str(stop_id))

        print(result)
        
    return HttpResponse(json.dumps(result))



