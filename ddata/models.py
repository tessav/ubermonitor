from __future__ import unicode_literals

from django.db import models

class Trip(models.Model):
    pickup = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    start_lat = models.DecimalField(max_digits=9, decimal_places=6)
    start_lon = models.DecimalField(max_digits=9, decimal_places=6)
    end_lat = models.DecimalField(max_digits=9, decimal_places=6)
    end_lon = models.DecimalField(max_digits=9, decimal_places=6)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.pickup + " - " + self.destination

class RideDetails(models.Model):
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    date = models.CharField(max_length=200)
    day = models.CharField(max_length=200)
    time = models.CharField(max_length=200)
    distance = models.FloatField(default=0)
    duration = models.IntegerField(default=0)
    high_est = models.IntegerField(default=0)
    low_est = models.IntegerField(default=0)
    estimate = models.CharField(max_length=200)

    def __str__(self):
        return self.estimate
