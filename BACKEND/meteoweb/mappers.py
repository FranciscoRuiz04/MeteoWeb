########################    Packages    ########################
import pandas as pd
import geopandas as gpd
import os
from dotenv import load_dotenv as env
env()

#-----------------------    GPS Pckgs    ----------------------#
import creators as cre


def urlCoords():
    """
    A generator to create a new URL for every coordindates pair
    extracted from stations shapefile.
    """
    
    shp = gpd.read_file(os.getenv('shp'))
    coords = (dict(north=row['POINT_Y'], east=row['POINT_X']) for _, row in shp.iterrows()) #Generator object with every coordinates pair
    for coord in coords:
        north = str(coord['north'])[:5] #Take only the two first decimals
        east = str(coord['east'])[:7]   #Take only the two first decimals
        url = "{}/es/tiempo/semana/{}N{}E".format(os.getenv('mainurl'), north, east)
        yield dict(url=url, city=(float(east), float(north)),path='ram')
