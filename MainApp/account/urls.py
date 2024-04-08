from django.urls import path
from .views import consultant_view,manager_view,financial_view,redirect_based_on_user_type,view_past_timesheets,view_timesheets,update_timesheet_entry
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('portal/', views.portal_view, name='portal'),
    path('logout/', views.logout_redirect, name='logout'),
    path('redirect/', redirect_based_on_user_type, name='redirect_user_type'),
    path('consultant/', consultant_view, name='consultant'),
    path('financial/', financial_view, name='financial'),
    path('manager/', manager_view, name='manager'),
    path('view_today_timesheet/', views.view_today_timesheet, name='timesheetview'),
    path('past-timesheets/', view_past_timesheets, name='view_past_timesheets'),
    path('timesheets/', view_timesheets, name='view_timesheets'),
    path('timesheets/update_entry/', update_timesheet_entry, name='update_timesheet_entry'),
    
    
]