########################    Packages    ########################

import json
# from dotenv import load_dotenv as env
from meteoweb import gps4cast
from datetime import datetime
import os
#--------------------------------------------------------------#

# env()  # Get enviroment variables from .env file

########################    Classes    ########################


class BetterPlace:

    def __init__(self, pathfile, url, cityname):
        self.path = pathfile
        self.url = url
        if cityname:
            self.city = cityname
        else:
            self.city = self.getcity()

    def getcity(self):
        place = self.url.split('/')[-1]
        city = place.split('_')[0]
        self.city = city
        return self.city


########################    Generator    ########################

def getPlaces(rootpath):
    with open(rootpath, 'r') as file:
        for place in json.load(file):
            yield place


########################    Functions    ########################

def newPlace(rootpath, pathfile, url, cityname=False):
    """
    Add places of interest into JSON file, of which going to be
    get its forecast, respectively.
    If JSON file doesn't exist, this will be created with the URL forecast 
    for Guanajuato City by default.
    """

    if not os.path.isdir(rootpath):
        firstobj = BetterPlace(os.getenv('mypath'),
                               os.getenv('starturl'), cityname)
        with open(rootpath, 'w') as nfile:
            json.dump([firstobj.__dict__], nfile, indent=4)

    newobj = BetterPlace(pathfile, url, cityname)
    with open(rootpath, 'r+') as cfile:
        content = json.load(cfile)
        content.append(newobj.__dict__)
        cfile.seek(0)
        json.dump(content, cfile, indent=4)


def dropPlace(rootpath, cityname):
    """
    Drop cityname properties to forecast from the root JSON file
    """

    places = getPlaces(rootpath)
    newcont = []
    for place in places:
        if place["city"] != cityname:
            newcont.append(place)
    with open(rootpath, 'w') as file:
        json.dump(newcont, file, indent=4)
#--------------------------------------------------------------#
