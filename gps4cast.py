########################    Packages    ########################

import sys
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv as env
#--------------------------------------------------------------#

env()  # Get constant values from .env file

########################    Generators    ########################


def _genLinks(item):
    for i in item:
        links = i.find('a')
        path = links.get('href')
        if path and path.startswith('/'):
            path = os.getenv('mainurl') + path
        yield path


def get_linked_urls(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    labels = (label for label in soup.find_all(class_='tab'))
    links = _genLinks(labels)
    for link in links:
        yield link


########################    Classes    ########################

class Daily4cast:

    def __init__(self, url, className="tab active"):
        self.url = url
        self._class = className
        try:
            _req = requests.get(self.url)
        except:
            raise Exception("Request failed!")
        else:
            _soup = BeautifulSoup(_req.content, 'html.parser')
            self.tag = _soup.find(class_=self._class)
            self.html = _soup

    def date_fun(self):
        """
        Get dates from 'time' tag.
        Outcome format is as follows: YYYY-MM-DD
        String type outcome
        """
        tag = self.tag.find('time')
        content = tag.get('datetime')
        self.date = content
        return self.date

    def tmp(self):
        """
        Get the temperature range from the text within 
        two different tags (tab-temp-max, tab-temp-min)
        A tuple is the outcome with the next format: (Min, Max)
        Both values are float type
        """
        maxTmp = self.tag.find(class_='tab-temp-max').text.strip()[:-3]
        minTmp = self.tag.find(class_='tab-temp-min').text.strip()[:-3]
        self.temp = (int(minTmp), int(maxTmp))
        return self.temp

    def wind_fun(self):
        """
        Get the text within tag with 'wind' as class name
        A tuple is the outcome with the next format: (Speed, Dir)
        Speed is a integer type
        Dir is a string type
        """
        patTag = self.tag.find(class_='wind')
        speed = patTag.text.strip()[:-5]
        direction = patTag.span['class'][-1]
        self.wind = (int(speed), direction)
        return self.wind

    def precip_fun(self):
        """
        Get precipitation from tag with 'tab-precip' class name
        Two kind of tuples could get:
        (pmin, pmax) or (None, None)
        Outcome (None, None) appears when doesn't have rain forecast
        """
        values = [l.strip() for l in self.tag.find(
            class_='tab-precip').text.split('-')]
        try:
            self.precip = (int(values[0]), int(values[1][:-3]))
        except:
            self.precip = (None, None)
        return self.precip

    def sunhrs(self):
        """
        Get sun hours from tag with 'tab-sun' class name
        Output data type is integer
        """
        value = self.tag.find(class_='tab-sun').text.strip()[:-2]
        self.sun = int(value)
        return self.sun

    def previsibility(self):
        """
        Get previsibility from tag with 'tab-predictability' class name
        Grade of previsibility as outcome
        Data type outcome is string
        """
        patTag = self.tag.find(class_='tab-predictability')['title']
        level = patTag.split(':')[1].strip().upper()
        self.prev = level
        return self.prev

    def predict(self):
        """
        Fetch all the variables considered by the class with just
        run this function.
        Variables will be saved in:
        self.date = Date
        self.temp = Temp Range
        self.wind = Wind Speed
        self.precip = Precipitation Range
        self.sun = Sun hours
        self.prev = Grade of previsibility
        """
        self.date_fun()
        self.tmp()
        self.wind_fun()
        self.precip_fun()
        self.sunhrs()
        self.previsibility()


class Last4cast(Daily4cast):
    def __init__(self, url, className="tab active last"):
        Daily4cast.__init__(self, url, className)


if __name__ == '__main__':
    ini = Daily4cast(
        r"https://www.meteoblue.com/es/tiempo/semana/guanajuato_m%c3%a9xico_4005270?day=1", 'tab active last')
    print(ini.tag)
    ini = Last4cast(
        r"https://www.meteoblue.com/es/tiempo/semana/guanajuato_m%c3%a9xico_4005270?day=7")
    print(ini.tag)
