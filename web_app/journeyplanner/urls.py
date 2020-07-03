from django.urls import path
from . import views #import views.py from current directory
from django.conf.urls import url, include


# view.home is the function we created in views.py which returns a HttpResponse
# stating that we have made it to the homepage
urlpatterns = [
    path('', views.home, name = 'home-page'),
    path('about/', views.about, name = 'about-page'),
    path('routeplanner/', views.routeplanner, name = 'routeplanner'),
    path('allroutes/', views.allroutes, name = 'allroutes'),
    path('leap/', views.leap, name = 'leap'),
    path('disruptions/', views.disruptions, name = 'disruptions'),
    path('tourist/', views.tourist, name = 'tourist'),
    url(r'^prediction/', views.prediction, name = 'prediction'),
    url(r'^planner/', views.planner, name = 'planner'),
]



# we have a urls module in made project 'dublin-bus'. 
# this will take our whole website which urls should send us to our journeyplanner app



# www.youtube.com/journeyplanner/routes?bus=41a&time=1700
# www.youtube.com/timetable/routes
# www.youtube.com/cats/routes