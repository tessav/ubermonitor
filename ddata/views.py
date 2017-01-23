from django.shortcuts import render
from django.http import HttpResponse
from ddata.models import Trip, RideDetails


def index(request):
    total = RideDetails.objects.all()
    for t in total:
        t.day = getDay(t.day)
        t.time = getTime(t.time)
    context = {
        'trip': Trip.objects.all(),
        'ridedetails': total
    }
    return render(request, 'ddata/index.html', context)

def getDay(x):
    return {
        'Monday': 1,
        'Tuesday': 2,
        'Wednesday': 3,
        'Thursday': 4,
        'Friday': 5,
        'Saturday': 6,
        'Sunday': 7
    }[x]

def getTime(y):
    return y[:2]
