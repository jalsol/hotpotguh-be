from django.db import models
from django.db.models import CASCADE


class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.CharField(max_length=256)


class Tree(models.Model):
    name = models.CharField(max_length=200)
    space = models.CharField(max_length=10)
    period = models.FloatField()
    temperature = models.IntegerField()
    upper_temperature = models.IntegerField(null=True)
    pH_level = models.FloatField()
    upper_pH_level = models.FloatField(null=True)
    moisture_level = models.CharField(max_length=10)
    upper_moisture_level = models.CharField(max_length=10, null=True)
    image_path = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    days_grown = models.IntegerField(default=0)
    milestones = models.CharField(max_length=65535, default='')
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)


class Vendor(models.Model):
    address = models.CharField(max_length=200)
    open_hour = models.CharField(max_length=5)
    closed_hour = models.CharField(max_length=5)
    favorite = models.BooleanField(default=False)
