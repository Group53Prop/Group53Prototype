from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('login/', views.login_view, name='login_view'),
    path('portal/', views.portal_view, name='portal'),
    path('logout/', views.logout_redirect, name='logout'),
    path('logout/', views.logout_view, name='logout'),
    
]