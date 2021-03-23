from django.shortcuts import render
from django.core.files import File
from bs4 import BeautifulSoup as bs
import requests
from urllib import request as req
from tempfile import NamedTemporaryFile
import csv
from .models import Pilot


def index(request):
    pilots = Pilot.objects.all()
    return render(request, 'index.html', {'pilots':pilots})

def get_image(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    req = requests.get(url, headers = headers)
    soup = bs(req.text, 'html.parser')
    img_list= []
    if soup.find(class_='image'):
        image = soup.find(class_='image', attrs='a')
        images = image.findChildren("img", recursive = True)
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
            if int(row[0]) > 212:
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
                    print(image_url)
                    if image_url:
                        img_temp = NamedTemporaryFile(delete = True)
                        img_temp.write(req.urlopen(image_url).read())
                        img_temp.flush()
                        pilot.image.save(f'{striped_image[-1]}.jpg', File(img_temp))
                print(pilot.driver_id, pilot.forename)
                pilot.save()

            
    return render(request, 'image.html')

"""
if not data_from_form.image:
    striped_image = str(data_from_form.cover).split('/')
    image_url = data_from_form.cover
    img_temp = NamedTemporaryFile(delete = True)
    img_temp.write(req.urlopen(image_url).read())
    img_temp.flush()
    data_from_form.image.save(striped_image[-1], File(img_temp))
"""
