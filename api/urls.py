from django.urls import path
from . import views
from django.conf import settings


urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path('vendors', views.get_all_vendors),
    path('vendor/<int:id>', views.get_single_vendor),
]
