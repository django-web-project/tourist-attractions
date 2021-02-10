from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'account'
urlpatterns = [
    # localhost:8000/account
    path('', views.check_login, name='check_login'),
    path('setting/', views.profile, name='profile'),
    path('my-list/', views.my_list, name='my_list')
]



