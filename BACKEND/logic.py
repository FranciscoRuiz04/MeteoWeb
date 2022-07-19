########################    Packages    ########################

import json
from dotenv import load_dotenv as env
import os

#--------------------------------------------------------------#

env()  # Get enviroment variables from .env file


########################    Classes    ########################


class BetterPlace:

    def __init__(self, targetpath, url, cityname):
        self.path = targetpath
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

def getPlaces(root):
    with open(root, 'r') as file:
        for place in json.load(file):
            yield place


########################    Functions    ########################


def newPlace(root, targetpath, url, cityname):
    """
    Add places of interest into JSON file, of which going to be
    get its forecast, respectively.
    If JSON file doesn't exist, this will be created with the URL forecast 
    for Guanajuato City by default.
    """

    if not os.path.exists(root):
        file = open(root, 'w')
        json.dump([], file, indent=4)
        file.close()

    newobj = BetterPlace(targetpath, url, cityname)
    with open(root, 'r+') as cfile:
        content = json.load(cfile)
        for obj in content:
            if newobj.city == obj["city"]:
                return (False, newobj.city)
        content.append(newobj.__dict__)
        cfile.seek(0)
        json.dump(content, cfile, indent=4)
        return (True, newobj.city)


def dropPlace(root, cityname):
    """
    Drop cityname properties to forecast from the root JSON file
    """

    places = getPlaces(root)
    newcont = []
    n = 0
    for place in places:
        if place["city"] != cityname:
            newcont.append(place)
        else:
            n += 1
    if n:
        with open(root, 'w') as file:
            json.dump(newcont, file, indent=4)
    return n
#--------------------------------------------------------------#


if __name__ == '__main__':
    newPlace(url=os.getenv('starturl'), root=os.getenv(
        'root'), targetpath=os.getenv('testdir'), cityname='sma')