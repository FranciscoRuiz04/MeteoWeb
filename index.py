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


class DairyForecast:
    
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
        lab = self.tag.find('time')
        content = lab.get('datetime')
        return content
    
    # @decorator
    def tmp(self):
        max = self.tag.find(class_='tab-temp-max').text.strip()[:-3]
        min = self.tag.find(class_='tab-temp-min').text.strip()[:-3]
        return (int(min), int(max))
    
    # @decorator
    def wind(self):
        patTag = self.tag.find(class_='wind')
        speed = patTag.text.strip()[:-5]
        direction = patTag.span['class'][-1]
        return (speed, direction)
    
    def precip(self):
        pass


if __name__=='__main__':
    url = r"https://www.meteoblue.com/es/tiempo/semana/guanajuato_m%c3%a9xico_4005270?day=3"
    ini = DairyForecast(url)
    print(ini.wind())
    # g = get_linked_urls(url)
    # for i in g: print(i)