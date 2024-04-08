from django.urls import path

from .views import view_notifications

app_name = 'notifications'

urlpatterns = [
    
    path('notifications/', view_notifications, name='notifications'),
    
    
]