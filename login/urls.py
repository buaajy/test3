
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url('index/', views.index),
    url('login/', views.login),
    url('register/', views.register),
    url('logout/', views.logout),

]
