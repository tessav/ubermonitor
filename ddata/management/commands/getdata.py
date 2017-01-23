import os
from datetime import datetime
from pytz import timezone
import pytz

# used to call Uber API and translate results
import requests
import urllib
import json

from django.core.management.base import BaseCommand
from ddata.models import Trip, RideDetails

class Command(BaseCommand):
    def _getdata(self):
        #'{:.6f}'.format(flo)
        s_lat = '37.451264'
        s_lon = '-122.18776'
        e_lat = '37.406859'
        e_lon = '-122.077563'

        tripObject = Trip.objects.get( pickup='Home', destination='Work' )

        server_token = 'aMWw3gWLiIIC6xiciXtGpLgTcApRWiOP4EPnMBi0'
        call = 'https://api.uber.com/v1/estimates/price?start_latitude=' + s_lat + '&start_longitude=' + s_lon + '&end_latitude=' + e_lat + '&end_longitude=' + e_lon + '&server_token=' + server_token

        q = requests.get(call)
        print (q)

        # timezone conversion
        now = datetime.now(tz=pytz.utc)
        t = now.astimezone(timezone('US/Pacific'))

        tempdata = q.json()
        pooldata = tempdata['prices'][0]

        # save ride
        r = RideDetails()
        r.trip = tripObject
        r.date = t.strftime('%y/%m/%d')
        r.time = t.strftime('%H:%M')
        r.day = t.strftime('%A')
        r.distance = pooldata['distance']
        r.duration = pooldata['duration']
        r.high_est = pooldata['high_estimate']
        r.low_est = pooldata['low_estimate']
        r.estimate = pooldata['estimate']
        r.save()
        print ('saved!')

    def handle(self, *args, **options):
        self._getdata()
