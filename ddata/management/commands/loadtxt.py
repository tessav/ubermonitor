import os
from datetime import datetime
from pytz import timezone
import pytz
import ast
import yaml

# used to call Uber API and translate results
import requests
import urllib
import json

import argparse

from django.core.management.base import BaseCommand
from ddata.models import Trip, RideDetails

class Command(BaseCommand):
    help = 'Parses txt file to add each ride estimate entry to database'

    def add_arguments(self, parser):
        parser.add_argument('--txt', help='Mech CSV file containing Chiplet Information')

    def handle(self, *args, **options):
        txtfile = options['txt']
        #print 'ERROR! PROPER MINIMUM FORMAT: python manage.py loadtxt --txt <TXT_FILENAME>'
        if os.path.isfile(txtfile):
            print 'file present'
            f = open(txtfile)
            data = f.readlines()
            for n in data:
                lal = n.rstrip('\n')
                colposition = lal.find(':')
                lal = lal[:colposition] + "'" + lal[colposition:]
                lal = lal[:1] + "u'" + lal[1:]
                outerdict = ast.literal_eval(lal)
                for d,pooldata in outerdict.items():
                    dt = datetime.strptime(d, 'datetime.datetime(%Y, %m, %d, %H, %M)')

                    r = RideDetails()
                    tripObject = Trip.objects.get( pickup='Home', destination='Work' )
                    r.trip = tripObject
                    r.date = dt.strftime('%y/%m/%d')
                    r.time = dt.strftime('%H:%M')
                    r.day = dt.strftime('%A')

                    r.distance = pooldata['distance']
                    r.duration = pooldata['duration']
                    r.high_est = pooldata['high_estimate']
                    r.low_est = pooldata['low_estimate']
                    r.estimate = pooldata['estimate']
                    r.save()

            f.close()
            # save ride

            print ('saved!')


        print "\nEntry Added!"
