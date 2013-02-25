from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)

class Coordinate(models.Model):
    user = models.ForeignKey(User)
    time = models.DateTimeField()
    latitude = models.IntegerField()
    longitude = models.IntegerField()
