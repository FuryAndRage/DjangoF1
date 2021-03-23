from django.shortcuts import render
from django.core.files import File
from bs4 import BeautifulSoup as bs
import requests
from urllib import request as req
from tempfile import NamedTemporaryFile
import csv
from .models import Constructors

# Create your views here.



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



def creator(request):
    with open('static/constructors.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        for row in csv_reader:
            constructor = Constructors(
                constructor_id  = row[0],
                constructor_ref = row[1],
                name = row[2],
                nationality = row[3],
                url = row[4],

            
            )
            if not constructor.image:
                striped_image = str(constructor.url).split('/')
                image_url = f'https:{get_image(row[-1])}'
                print(image_url)
                if image_url:
                    img_temp = NamedTemporaryFile(delete = True)
                    img_temp.write(req.urlopen(image_url).read())
                    img_temp.flush()
                    constructor.image.save(f'{striped_image[-1]}.jpg', File(img_temp))
            print(constructor.name)
            constructor.save()

            
    return render(request, 'image.html')
