from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Pilot
from DjangoF1.apps.constructor_season.models import ConstructorSeason
from DjangoF1.apps.constructor.models import Constructors
from DjangoF1.apps.pilot_season.models import PilotSeason
import json


def get_json_driver_standing_season(season):
    with open(f'static/driver_standing/driver_standing_{season}.json', 'r') as fs:
        data = json.load(fs)
        new_dict = []
        standings_list = []
        standings_dict = dict()
        for item in data.values():
            for i,x in item.items():
                new_dict.append(x)

        for item in new_dict[-1]['StandingsLists'][0]['DriverStandings']:
            constructor = get_object_or_404(Constructors, constructor_ref = item.get('Constructors')[0]['constructorId'])
            standings_dict = {
                'driver':get_object_or_404(Pilot, driver_ref = item.get('Driver')['driverId']),
                'constructor':get_object_or_404(Constructors, constructor_ref = item.get('Constructors')[0]['constructorId']),
                'constructor_season': ConstructorSeason.objects.filter(Q(season = season) & Q(constructor = constructor.id) ),
                'position':item.get('position'),
                'points':item.get('points'),
                'wins': item.get('wins')
                }

            standings_list.append(standings_dict)

        return standings_list


def get_json_driver_season(season):
    with open(f'static/drivers/drivers_season_{season}.json', 'r') as fs:
        data = json.load(fs)
        new_dict = []
        drivers_list = []
        drivers_dict = dict()
        for item in data.values():
            for i,x in item.items():
                new_dict.append(x)

        for item in new_dict:
            print(item)
        for item in new_dict[-1].get('Drivers'):
            
            drivers_dict = {
                'driver':get_object_or_404(Pilot, driver_ref = item['driverId']),
                }
            drivers_list.append(drivers_dict)

        return drivers_list


def get_json_current_driver_standing():
    with open(f'static/drivers/drivers_current.json', 'r') as fs:
        data = json.load(fs)
        standings_list = []
        standings_dict = dict()
        gen_list = [item['StandingsTable'] for item in data.values()]
        for item in gen_list[-1].get('StandingsLists'):
            season = item.get('season')
            for driver in item.get('DriverStandings'):
                constructor = get_object_or_404(Constructors, constructor_ref = driver.get('Constructors')[0]['constructorId'])
                pilot = get_object_or_404(Pilot, driver_ref = driver.get('Driver')['driverId'])
                standings_dict = {
                    'driver': pilot,
                    'constructor':get_object_or_404(Constructors, constructor_ref = driver.get('Constructors')[0]['constructorId']),
                    'constructor_season': ConstructorSeason.objects.filter(Q(season = season) & Q(constructor = constructor.id) ),
                    'pilot_season': PilotSeason.objects.filter(Q(season = season) & Q(pilot = pilot.id)),
                    'position':driver.get('position'),
                    'points':driver.get('points'),
                    'wins': driver.get('wins')
                    }
                standings_list.append(standings_dict)

        return standings_list