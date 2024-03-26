# timesheet/urls.py
from django.urls import path
from .views import my_view, clock_in, clock_out


app_name = 'timesheet'  

urlpatterns = [
    path('my-view/', my_view, name='my_view'), 
    path('clock-in/', clock_in, name='clock_in'),
    path('clock-out/', clock_out, name='clock_out'),   
    
]
