import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys
import os
from dotenv import load_dotenv as env

env()   #Get constant values from .env file

def genLinks(item):
    for i in item:
        links = i.find('a')
        path = links.get('href')
        if path and path.startswith('/'):
            path = os.getenv('main') + path
        yield path

def get_linked_urls(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    labels = (label for label in soup.find_all(class_='tab'))
    links = genLinks(labels)
    for link in links:
        yield link


class DailyForecast:
    
    def __init__(self, url, className = "tab active"):
        self.url = url
        self._class = className
        try:
            _req = requests.get(self.url)
        except:
            raise Exception("Request failed!")
        else:
            _soup = BeautifulSoup(_req.content, 'html.parser')
            self.tag = _soup.find(class_=self._class)
        
    def date(self):
        tag = self.tag.find('time')
        content = tag.get('datetime')
        self.d = content
        return self.d
    
    def tmp(self):
        maxTmp = self.tag.find(class_='tab-temp-max').text.strip()[:-3]
        minTmp = self.tag.find(class_='tab-temp-min').text.strip()[:-3]
        self.temp = (int(minTmp), int(maxTmp))
        return self.temp
    
    def wind(self):
        patTag = self.tag.find(class_='wind')
        speed = patTag.text.strip()[:-5]
        direction = patTag.span['class'][-1]
        self.w = (speed, direction)
        return self.w
    
    def precip(self):
        value = self.tag.find(class_='tab-precip').text.strip()[:-3].split('-')
        self.p = (value[0], value[1])
        return self.p
    
    def sunhrs(self):
        value = self.tag.find(class_='tab-sun').text.strip()[:-2]
        self.sun = value
        return self.sun
    
    def previsibility(self):
        patTag = self.tag.find(class_='tab-predictability')['title']
        level = patTag.split(':')[1].strip().upper()
        self.prev = level
        return self.prev
    
    def predict(self):
        self.date()
        self.tmp()
        self.wind()
        self.precip()
        self.sunhrs()
        self.previsibility()

if __name__=='__main__':
    url = os.getenv('starturl')
    ini = DailyForecast(url)
    ini.predict()
    print(ini.temp)