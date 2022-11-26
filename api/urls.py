from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('', views.get_user),
    path('login', views.login),
    path('register', views.register),
]
