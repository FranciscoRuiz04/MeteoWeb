__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


########################    Packages    ########################
from concurrent.futures import ProcessPoolExecutor
import geopandas as gpd
import pandas as pd
import os
from dotenv import load_dotenv as env
env()

#-----------------------    GPS Pckgs    ----------------------#
import collectors as coll


def urlCoords():
    """
    Generator to create a new URL for every coordindates pair
    extracted from a *.shp file.
        This object generates a Dictionary format type object
    as outcome with url for seven and forteen days forecast
    and its respective (x, y) coordinates pair. Its labels are:\n
        url7 -> URL to seven days forecast\n
        url14 -> URL to forteen days forecast\n
        point -> (x, y) coordinates pair\n
    """
    
    shp = gpd.read_file(os.getenv('shp'))
    coords = (dict(north=row['POINT_Y'], east=row['POINT_X']) for _, row in shp.iterrows()) #Generator object with every coordinates pair
    for coord in coords:
        north = round(coord['north'], 2) #Take only the two first decimals
        east = round(coord['east'], 2)   #Take only the two first decimals
        url_7 = "{}/es/tiempo/semana/{}N{}E".format(os.getenv('mainurl'), str(north), str(east))
        url_14 = "{}/es/tiempo/14-dias/{}N{}E".format(os.getenv('mainurl'), str(north), str(east))
        yield dict(url7=url_7, url14=url_14, point=[east, north])

class AttsSeven:
    """
    
    """
    
    def __init__(self, day, z):
        self.day = day - 1
        
        dictKeys = ['pp', 'p', 'tmin', 'tmax', 'ws', 'wd', 'date']
        equivalence = dict(zip(dictKeys, range(7)))
        self.zindex = equivalence[z]
        
        if day == 7:
            self.islast = True
        else:
            self.islast = False
        
    def getRec(self, location):
        city = coll.Brief(location['url7'])
        url = city.urls[self.day]
        z_value = city.genArray(url, self.islast)
        coords = location['point']
        coords.insert(0, z_value[self.zindex])
        return coords

    def getAtts(self):
        with ProcessPoolExecutor(max_workers=15) as exec:
            results = exec.map(self.getRec, urlCoords())
            atts = pd.DataFrame(columns=['value', 'long', 'lat'])
            for result in results:
                atts.loc[len(atts)] = result
        return atts


if __name__ == '__main__':
    import time
    t1 = time.perf_counter()
    
    ini = AttsSeven(2, 'p')
    
    print(ini.getAtts().head())
    t2 = time.perf_counter()
    print(t2-t1)
    