"""
URL configuration for MainApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from account.views import redirect_based_on_user_type
from django.urls import include, path
from timesheet.views import (
    my_view
)
from account.views import(

    consultant_view,manager_view,financial_view,redirect_based_on_user_type,
    view_past_timesheets,view_timesheets
   
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', my_view,name="home"),
    path('account/', include('account.urls', namespace='account')),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='login'),
    path('timesheet/', include('timesheet.urls', namespace='timesheet')),
    path('redirect/', redirect_based_on_user_type, name='redirect_user_type'),
    path('consultant/', consultant_view, name='consultant'),
    path('financial/', financial_view, name='financial'),
    path('manager/', manager_view, name='manager'),
    path('past-timesheets/', view_past_timesheets, name='view_past_timesheets'),
    path('timesheets/', view_timesheets, name='view_timesheets'),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    

    
    

    
    
    
]
