import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

def genLinks(item):
    for i in item:
        links = i.find('a')
        path = links.get('href')
        if path and path.startswith('/'):
            path = 'https://www.meteoblue.com' + path
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
    
    # def decorator(fun):
    #     def wrap(self):
    #         global _label
    #         req = requests.get(self.url)
    #         soup = BeautifulSoup(req.content, 'html.parser')
    #         _label = soup.find(class_=self._class)
    #         return fun()
    #     return wrap    
    
    # @decorator
    def date(self):
        tag = self.tag.find('time')
        content = tag.get('datetime')
        return content
    
    # @decorator
    def tmp(self):
        maxTmp = self.tag.find(class_='tab-temp-maxTmp').text.strip()[:-3]
        minTmp = self.tag.find(class_='tab-temp-minTmp').text.strip()[:-3]
        return (int(minTmp), int(maxTmp))
    
    # @decorator
    def wind(self):
        patTag = self.tag.find(class_='wind')
        speed = patTag.text.strip()[:-5]
        direction = patTag.span['class'][-1]
        return (speed, direction)
    
    def precip(self):
        tag = self.tag.find(class_='tab-precip').text.strip()[:-3].split('-')
        return (tag[0], tag[1])
    
    def sunhrs(self):
        tag = self.tag.find(class_='tab-sun').text.strip()[:-2]
        return tag
    
    def previsibility(self):
        patTag = self.tag.find(class_='tab-predictability')['title']
        level = patTag.split(':')[1].strip().upper()
        return level

if __name__=='__main__':
    url = r"https://www.meteoblue.com/es/tiempo/semana/guanajuato_m%c3%a9xico_4005270?day=5"
    ini = DailyForecast(url)
    print(ini.date())
    # g = get_linked_urls(url)
    # for i in g: print(i)