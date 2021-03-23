from django.shortcuts import render
from django.core.files import File
from bs4 import BeautifulSoup as bs
import requests
from urllib import request as req
from tempfile import NamedTemporaryFile
import csv

import xmltodict, json

def season(request, season):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
    req = requests.get(f'http://ergast.com/api/f1/{season}/driverStandings', headers = headers)
    
    parsed_xml = xmltodict.parse(req.text)
    dumped_json = json.dumps(parsed_xml)
    print(req.text)
    # print(dict(parsed_xml))
    return render(request, 'season.html')


# get_json('http://ergast.com/api/f1/2020/drivers')
# get_json('http://ergast.com/api/f1/2020/driverStandings')