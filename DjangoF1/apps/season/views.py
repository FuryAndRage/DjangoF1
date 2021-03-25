from django.shortcuts import render, get_object_or_404
from DjangoF1.apps.constructor.models import Constructors
from DjangoF1.apps.pilot.models import Pilot
import requests
import os
import  json

def get_json(season):
    with open(f'static/driver_standing_{season}.json', 'r') as fs:
        data = json.load(fs)
        new_dict = []
        standings_list = []
        standings_dict = dict()
        for item in data.values():
            for i,x in item.items():
                new_dict.append(x)

        for item in new_dict[-1]['StandingsLists'][0]['DriverStandings']:
            standings_dict = {
                'driver':get_object_or_404(Pilot, driver_ref = item.get('Driver')['driverId']),
                'constructor':get_object_or_404(Constructors, constructor_ref = item.get('Constructors')[0]['constructorId']),
                'position':item.get('position'),
                'points':item.get('points'),
                'wins': item.get('wins')
                }

            standings_list.append(standings_dict)
            
            # print(item)
        for item in standings_list:
            print(item.get('driver'), item.get('position'), item.get('points'))
        

def season(request, season):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    req = requests.get(f'http://ergast.com/api/f1/{season}/driverStandings.json', headers = headers)
    
    if os.path.isfile(f'static/driver_standing_{season}.json'):
       get_json(season)
    else:
        with open(f'static/driver_standing_{season}.json', 'wb') as file:
            file.write(req.content)
            get_json(season)

       
  

    
    return render(request, 'season.html')


# get_json('http://ergast.com/api/f1/2020/drivers')
# get_json('http://ergast.com/api/f1/2020/driverStandings')