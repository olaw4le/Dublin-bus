from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.http import HttpResponse, JsonResponse
import sys
sys.path.append("..")
from .route_details import stops_latlng, find_stop,latlng
import requests
import json
import requests
from pyleapcard import *
from .fare import get_fare

from data_analytics import linear_regression_weather
from data_analytics import get_direction
from data_analytics import db_interface
from data_analytics import get_journey_proportion as jp
from data_analytics.to_time_group import to_time_group

from datetime import datetime, timedelta, time


sys.path.append("..")


# showing how data can be added to a html page
posts = [
    {
        'from': 'Charlestown',
        'to': 'Limekiln Avenue',
        'time': '10:40'
    },
    {
        'route': 'Route 39',
        'from': 'Burlington Road',
        'to': 'Ongar',
        'time': '07:00'
    }
]


# create home function to handle traffic from journeyplanner app
# return what we want the user to see when they are sent to this route


# request arg has to be here
def home(request):
    # context is a dictionary. the keys will be accessible from within the home.html template
    context = {
        'posts': posts
    }
    # context is given as argument. This passes that data into the home template
    # posts variable will now be accessible from within home.html
    return render(request, 'journeyplanner/home.html', context) # render still returns a HttpResponse


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


def realtime(request):
    # can also pass dictionary in directly as arg
    return render(request, 'journeyplanner/realtime.html')


@csrf_exempt
def prediction(request):
    if request.method == "POST":
        route= request.POST["route"]
        origin= request.POST["origin"]
        destination = request.POST["destination"]
        date = request.POST["date"]
        time = request.POST["time"]
        direction=request.POST["direction"]
        print("From prediction(views.py): ", route, origin, destination, date, time)

        result = linear_regression_weather.generate_prediction(route, origin, destination, date, time, direction)
        print("Users estimated journey in minutes (from views.py)", result)


        journey_fare = get_fare(route, direction, origin, destination)
        results_dict = {"result" : result, "fare" : journey_fare}
        
    return JsonResponse(results_dict)


@csrf_exempt
def planner(request):
    if request.method == "POST":
        data= json.loads(request.POST["data"])
        
        prediction_and_fare = {}
        prediction=[] #list to store the calculated predictions
        
        # list of fare dictionaries containing fare, route and url for each bug leg of journey
        total_fare = []

        for i in data:

            route= i["route_number"]
            date = request.POST["date"]
            time = request.POST["time"]
            duration=i["duration"]

            print("duration",duration)

            #direction= 2
            route_number=route.upper()

            #departure stops lat and lng
            departure=i["departure_latlng"]
            x=departure.split(",")
            departure_lat = float(x[0])
            departure_lng = float(x[1])

            #arrival stops lat and lng
            arrival=i["arrival_latlng"]
            y=arrival.split(",")
            arrival_lat = float(y[0])
            arrival_lng = float(y[1])


            route_number=route.upper()
            # getting the suggested route file
            try:
                route_list=stops_latlng(route_number)
            except:
                route_list= 0
                
            
            try:
                #getting the orging and destination stop number using the vincenty formular
                origin=find_stop(route_list,(departure_lat,departure_lng))
                arrival=find_stop(route_list,(arrival_lat,arrival_lng))
                direction = get_direction.get_direction_from_stops(route, origin, arrival)
                print(direction)

            except:
                direction = None
                origin=0
                arrival=0

  

            #use the maachine learning module to calculate prediction
            try:
                calculation=linear_regression_weather.generate_prediction(route_number, origin, arrival, date, time, direction)
                prediction.append(calculation)
                print('prediction from module',prediction)
            except:
                prediction.append(duration)

            #adding the calculated value to the list that will be sent back
            # finally:
            #     pass
                


        # #get the fare for each leg of the journey
            journey_fare = get_fare(route, direction, origin, arrival)
            total_fare.append(journey_fare)
            

        
        print("prediction list",prediction)

    
    prediction_and_fare["fare"] = total_fare
    prediction_and_fare["prediction"] = prediction
    print("prediction and fare dict")
    print(prediction_and_fare)
    return JsonResponse(json.dumps(prediction_and_fare), safe=False)
    

@csrf_exempt
def find_latlng(request):
    if request.method == "POST":
        route = request.POST["route"]
        stop_id = request.POST["stop"]
        route_number = route.upper()

        # getting the suggested route file 
        route_list = stops_latlng(route_number)
        result = latlng(route_list, str(stop_id))

        print(result)
        
    return HttpResponse(json.dumps(result))


@csrf_exempt
def list_latlng(request):
    if request.method == "POST":
        route = request.POST["route"]
        route_number = route.upper()

        # getting the suggested route file 
        route_list = stops_latlng(route_number)
    return HttpResponse(json.dumps(route_list))


@csrf_exempt
def real_time(request):
    if request.method == "POST":
        stop_number = request.POST["stopnumber"]
        url = "https://data.smartdublin.ie/cgi-bin/rtpi/realtimebusinformation?stopid={}&format=json".format(stop_number)
        r = requests.get(url=url)

        data = r.json()
        print(data)

    return HttpResponse(json.dumps(data))


# csrf exemption is only temporary while running on local machine!!!
@csrf_exempt
def leap_login(request):

    if request.method == "POST":
        user = request.POST["user"]
        password = request.POST["passwd"]

        leap_session = LeapSession()

        # attempt to login to www.leapcard.ie with supplied credentials
        # return error if credentials are incorrect
        try:
            leap_session.try_login(user, password)

        except Exception as e:
            print(e)
            return e

        # request the www.leapcard.ie account overview
        overview = leap_session.get_card_overview()
        stats = {"cardNumber": overview.card_num, "cardBalance": overview.balance, "cardName": overview.card_label,
                 "cardType": overview.card_type, "cardExpiry": overview.expiry_date}

        # convert stats to json format & return to user
        return HttpResponse(json.dumps(stats))


# csrf exemption is only temporary while running on local machine!!!
@csrf_exempt
def get_stats(request):

    def round_time(time_str):
        """ takes a passed 24 hr time in the string format 'HH:MM' and returns a
        string representation of that time rounded to the nearest 30 minutes"""

        split_str = time_str.split(":")
        hours, minutes = split_str[0], int(split_str[1])

        # if minutes is closer to half-hour than full hour then round to half-hour
        if 15 < minutes < 45:
            minutes = "30"
        # else round to nearest hour
        else:
            if minutes >= 45:
                if hours != 23:
                    hours = str(hours + 1).zfill(2)
                else:
                    hours = "00"
            minutes = "00"

        return "%s:%s" % (hours, minutes)

    if request.method == "POST":

        date_str = request.POST["date"]
        time_str = request.POST["time"]
        route = request.POST["route"]
        origin = request.POST["start"]
        destination = request.POST["end"]
        direction = request.POST["direction"]

        # extract the month & weekday from the date
        # need to do this for each time tested...
        # time_obj = time(second=int(time_str))
        time_obj = time.fromisoformat("%s:00" % time_str)
        date_obj = datetime.fromisoformat("%s %s" % (date_str, time_obj.strftime("%H:%M:%S")))

        "2020-07-23"    # date format
        "73740"         # time format

        # determine the segments on this route
        all_stops = jp.stops_on_route(str(route), main=True, direction=int(direction))
        sub_stops = jp.stops_on_journey(origin, destination, all_stops)
        sub_segments = jp.segments_from_stops(sub_stops)

        # template for the response json
        response = {
            hourly: {},
            daily: {}
        }

        # for an hour either side of the searched time groups - estimate the journey time based on historical averages
        offsets = [-3600, -1800, 0, 1800, 3600]

        for n in offsets:
            # create a time delta object representing a difference of n seconds
            offset = timedelta(0, n)
            dt = date_obj + offset

            time_str = round_time(dt.strftime("%H:%M"))
            month = dt.strftime("%B")
            weekday = dt.strftime("%A")

            # get the daytime as number of seconds since midnight & convert into 'time group'
            time_group = to_time_group(int((dt - datetime.fromisoformat(dt.strftime("%Y-%m-%d"))).total_seconds()))

            # add the estimated journey time to this the response dict (convert into minutes)
            response["hourly"][time_str] = jp.get_95_percentile(route, direction, sub_segments,
                                                                month, weekday, time_group) // 60

        # for 3 days either side of the searched day - estimate journey duration at this time of day
        offsets = [-3, -2, -1, 0, 1, 2, 3]

        for n in offsets:
            # create a time delta object representing a difference of n seconds
            offset = timedelta(n)
            dt = date_obj + offset

            weekday_short = dt.strftime("%a")
            month = dt.strftime("%B")
            weekday = dt.strftime("%A")

            # get the daytime as number of seconds since midnight & convert into 'time group'
            time_group = to_time_group(int((dt - datetime.fromisoformat(dt.strftime("%Y-%m-%d"))).total_seconds()))

            # add the estimated journey time to this the response dict (convert into minutes)
            response["daily"][weekday_short] = jp.get_95_percentile(route, direction, sub_segments,
                                                                    month, weekday, time_group) // 60

        print(response)
        return HttpResponse(json.dumps(response))

