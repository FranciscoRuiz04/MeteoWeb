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
import cloupy as cp
import numpy as np
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
    
    shp = gpd.read_file(os.getenv('stats'))
    coords = (dict(north=row['POINT_Y'], east=row['POINT_X']) for _, row in shp.iterrows()) #Gen objt with every coordinates pair
    for coord in coords:
        north = round(coord['north'], 2) #Take only the two first decimals
        east = round(coord['east'], 2)   #Take only the two first decimals
        url_7 = "{}/es/tiempo/semana/{}N{}E".format(os.getenv('mainurl'), str(north), str(east))
        url_14 = "{}/es/tiempo/14-dias/{}N{}E".format(os.getenv('mainurl'), str(north), str(east))
        yield dict(url7=url_7, url14=url_14, point=[east, north])

class AttSeven:
    """
    A object to generate a Dataframe object type with the
    attributes table format for the next 7 days forecast.
        Object needs two parameters; day and meteorological
    variable.
        day -> Forecast day\n
        z -> Meteorological variable wanted\n
    
    Z parameter could take one of the following arguments
        pp = precipitation probability in percentaje\n
        p = precipitation in mm\n
        tmin = minimum temperature in Celcius Degrees\n
        tmax = maximum temperature in Celius Degrees\n
        ws = wind speed in kilometres per hour\n
        wd = wind direction. (NW, NE, SW, SE)\n
        date = date. (YYYY-MM-DD)\n
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
        """
        Get a list format type with the respective value
        and its location coordinates; longitude and latitude.
        [value, long, lat].
            Take one parameter which needs to be a dictionary
        with a key named url7.
        """
        
        city = coll.Brief(location['url7'])
        url = city.urls[self.day]
        z_value = city.genArray(url, self.islast)
        coords = location['point']
        coords.insert(0, z_value[self.zindex])
        return coords

    def getAtts(self):
        """
        Get a pandas.Dataframe object with the meteorological
        values and its respective coordinates pair (longitude,
        latitude) for every point within a shapefile.
            Heads are:\n
        z_value = Forecasted value
        lon = Longitude
        lat = Latitude
        """
        
        with ProcessPoolExecutor(max_workers=15) as exec:
            results = exec.map(self.getRec, urlCoords())
            atts = pd.DataFrame(columns=['z_value', 'lon', 'lat'])
            for result in results:
                atts.loc[len(atts)] = result
        return atts


class Mappers:
    """
    
    """
    
    def __init__(self, day, z):
        self.attsTable = AttSeven(day, z).getAtts()
    
    def toMap(self, method='default'):
        minVal = self.attsTable['z_value'].min()
        maxVal = self.attsTable['z_value'].max()
        imap = cp.m_MapInterpolation(shapefile_path=os.getenv('bounds'), dataframe=self.attsTable, crs='epsg:4326')
        imap.draw(
        levels=np.arange(minVal, maxVal + 1, 0.1), # (start, end, step),
        zoom_in=[(-102.2, -99.6), (19.87, 21.9)],
        # show_points=True,
        interpolation_method='cubic',
        cbar_title='Temperatura Mínima (°C)',
        title='Pronóstico meteorológico para el estado de Guanajuato\n18 de enero, 2023.',
        title_ha='center',
        title_x_position=0.5,
        save='map_Mappers.png'
        )


if __name__ == '__main__':
    ini = Mappers(2, 'tmin')
    ini.toMap()
    # ini.getAtts().to_csv('data.csv', index=False)