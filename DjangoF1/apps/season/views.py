from django.shortcuts import render
from django.core.files import File
from bs4 import BeautifulSoup as bs
import requests
from urllib import request as req
from tempfile import NamedTemporaryFile
import csv
import os

import xml.etree.ElementTree as ET

import xmltodict, json

def season(request, season):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    req = requests.get(f'http://ergast.com/api/f1/{season}/driverStandings', headers = headers)
    
    parsed_xml = xmltodict.parse(req.content)
    dumped_json = json.dumps(parsed_xml)
    if os.path.isfile(f'static/driver_standing_{season}.xml'):
        print('ja existe')
    else:
        print('vou criar agora')
        with open(f'static/driver_standing_{season}.xml', 'wb') as file:
            file.write(req.content)

    with open(f'static/driver_standing_{season}.xml', 'r') as fs:
        mydoc = xmltodict.parse(fs.read())
        json_file = json.dumps(mydoc)
        with open(f'static/driver_standing_{season}.json', 'w') as js:
            js.write(json_file)
    with open(f'static/driver_standing_{season}.json', 'r') as f:
        data = json.load(f)
        for item in data.values():
            for i in item.keys():
                print(i)
           
  

    # mydoc = f'static/driver_standing_{season}.xml'
    # tree = ET.parse(mydoc)
    # root = tree.getroot()
    # filter = '*'
    # for child in root.iter():
    #     file = {child.tag:child.text}
    #     print(file)
    
    return render(request, 'season.html')


# get_json('http://ergast.com/api/f1/2020/drivers')
# get_json('http://ergast.com/api/f1/2020/driverStandings')