from django.contrib import admin
from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.home),
    path('disease', views.disease),
    path('predict', views.predict, name="predict"),
    path('home', views.home, name="home"),
    path("register", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name= "logout"),
    path('appointment', views.appointment, name = "appointment"),
    path('appointment_result', views.appointment_result, name = "appointment_result"),
    path('doctor', views.get_data, name = "get_data"),


]
