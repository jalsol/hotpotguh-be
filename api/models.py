from django.db import models
from django.db.models import CASCADE


class User(models.Model):
    username = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=200, default='')
    email = models.CharField(max_length=32, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    password = models.CharField(max_length=256)


class BaseTree(models.Model):
    name = models.CharField(max_length=200)
    space = models.CharField(max_length=10)
    period = models.FloatField()
    period_display = models.CharField(max_length=50)
    temperature = models.IntegerField()
    upper_temperature = models.IntegerField(null=True)
    pH_level = models.FloatField()
    upper_pH_level = models.FloatField(null=True)
    moisture_level = models.CharField(max_length=10)
    upper_moisture_level = models.CharField(max_length=10, null=True)
    image_path = models.CharField(max_length=200)
    description = models.CharField(max_length=500, default='')

    def __str__(self):
        return str(self.pk)


class Tree(models.Model):
    base = models.ForeignKey(BaseTree, on_delete=CASCADE)
    days_grown = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=CASCADE, null=True)


class Vendor(models.Model):
    name = models.CharField(max_length=200)
    district = models.CharField(max_length=20)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=15)
    business_hours = models.CharField(max_length=5)
    rating = models.FloatField()
    favorite = models.BooleanField(default=False)
