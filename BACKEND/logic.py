__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

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


def attsFromFile(pathfile, sep=None, headers=False, iloc=[1, 2], encod='utf-8'):
    """
    Get a dictionary type object with the attributes from a csv file for every
    new record to be added into cities forecasted database.
    CSV file must have 2 columns at least: one with the url and another one
    with the save targetpath where will be saved the data scrapped from the
    web.

    Parameters:
    <<pathfile>> a string with the path file.
    
    <<sep>> character which separate every field. Is not define by default.

    <<headers>> indicates if the file have headers. By default is False.

    <<iloc>> is a list type object with the column number where is every
    corresponding attribute. The order of indexes corresponds as follow:
    [url, folder, name]. By default takes the order [1, 2].
    For example:
    [2,1] indicates that url is in the second column and the targetpath folder
    information is in the column number one. 
    
    <<encod>> File encoding. By defaul is UTF-8.

    """

    attributes = {}
    
    with open(pathfile, 'r', encoding=encod) as file:
        lines = (line.split(sep) for line in file)
        if headers:
            next(lines)
        for line in lines:
            atts = [att.strip("\n\ufeff") for att in line]
            
            attributes['url'] = atts[iloc[0]-1]
            attributes['name'] = atts[iloc[1]-1]
            yield attributes

#--------------------------------------------------------------#


if __name__ == '__main__':
    # newPlace(url=os.getenv('starturl'), root=os.getenv(
    #     'root'), targetpath=os.getenv('testdir'), cityname='sma')
    pipline = ((att['url'], att['name']) for att in attsFromFile('c:/usersfrancisco ruiz/desktop/example.csv',','))
    print(next(pipline))