from django.shortcuts import render,get_object_or_404
from django.core.files import File
from django.db.models import Q
from bs4 import BeautifulSoup as bs
import requests
from urllib import request as req
from tempfile import NamedTemporaryFile
import csv
from .models import Pilot
import time
import json
import os

from DjangoF1.apps.constructor_season.models import ConstructorSeason
from DjangoF1.apps.constructor.models import Constructors

def index(request):
    pilots = Pilot.objects.all()
    return render(request, 'index.html', {'pilots':pilots})

def get_json(season):
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

def driver_standing_by_season(request, season):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    req = requests.get(f'http://ergast.com/api/f1/{season}/driverStandings.json', headers = headers)
    
    if os.path.isfile(f'static/driver_standing/driver_standing_{season}.json'):
       return render(request, 'driver_standing.html', {'stats':get_json(season)})
    else:
        with open(f'static/driver_standing/driver_standing_{season}.json', 'wb') as file:
            file.write(req.content)
            get_json(season)

            return render(request, 'driver_standing.html', {'stats':get_json(season)})



def get_image(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    req = requests.get(url, headers = headers)
    soup = bs(req.text, 'html.parser')
    img_list= []
    if soup.find(class_='vcard'):
        vcard = soup.find(class_='vcard')
        if vcard.find(class_='image'):
            image = soup.find_all(class_='image', attrs='a')
            if len(image) > 1:
                images = image[0].findChildren("img", recursive = True)
                if(images[0].has_attr('srcset')):
                    images = images[0].get('srcset')
                else:
                    images = images[0].get('src')
            else:
                images = image[0].findChildren("img", recursive = True)
                if(images[0].has_attr('srcset')):
                    images = images[0].get('srcset')
                else:
                    images = images[0].get('src')
            srcset = images.split(',')
            [img_list.append(item.split()[0]) for item in srcset ]
    if len(img_list) > 0 :
        return img_list[0]
    else:
        return '//image.shutterstock.com/image-vector/ui-image-placeholder-wireframes-apps-260nw-1037719204.jpg'



def save_pilot(request):
    with open('static/drivers.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        for row in csv_reader:
            pilot = Pilot(
                driver_id = row[0],
                driver_ref = row[1],
                number = row[2],
                code = row[3],
                forename = row[4],
                surname = row[5],
                dob = row[6],
                nationality = row[7],
                url = row[8],
                

            )
            if not pilot.image:
                striped_image = str(pilot.url).split('/')
                image_url = f'https:{get_image(row[-1])}'
                if image_url:
                    img_temp = NamedTemporaryFile(delete = True)
                    img_temp.write(req.urlopen(image_url).read())
                    img_temp.flush()
                    pilot.image.save(f'{striped_image[-1]}.jpg', File(img_temp))
            print(pilot.driver_id, pilot.forename)
            pilot.save()
            

            
    return render(request, 'image.html')

def delete_pilot(request):
    for item in Pilot.objects.all():
        item.delete()
    return render(request, 'image.html')