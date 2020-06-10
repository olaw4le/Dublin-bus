from django.shortcuts import render

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

