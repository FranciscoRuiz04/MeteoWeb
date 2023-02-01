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
from . import collectors as coll
from . import interpolation_methods as interpol


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
    coords = (dict(north=row['POINT_Y'], east=row['POINT_X'])
              for _, row in shp.iterrows())  # Gen objt with every coordinates pair
    for coord in coords:
        north = round(coord['north'], 2)  # Take only the two first decimals
        east = round(coord['east'], 2)  # Take only the two first decimals
        url_7 = "{}/es/tiempo/semana/{}N{}E".format(
            os.getenv('mainurl'), str(north), str(east))
        url_14 = "{}/es/tiempo/14-dias/{}N{}E".format(
            os.getenv('mainurl'), str(north), str(east))
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
    """

    def __init__(self, day, z):
        self.day = day - 1

        dictKeys = ['pp', 'p', 'tmin', 'tmax', 'ws', 'wd', 'date']
        equivalence = dict(zip(dictKeys, range(7)))
        self.zindex = equivalence[z]
        self.z = z

        if day == 7:
            self.islast = True
        else:
            self.islast = False

    def getRec(self, location):
        """
        Get a dictionary with two elements.\n
            attribute -> A list format type object with z values
        and its location coordinates; longitude and latitude
        [z_value, long, lat].\n
            date -> Date data type (YYYY-MM-DD).\n
            variable -> Meteorological Variable.\n
            Takes one parameter which needs to be a dictionary
        with a key named url7.
        """
        
        variables = {'pp':('Probabilidad de Precipitación', '%'), 'p':('Precipitación', 'Milímetros de lluvia (mm)'), 'tmin':('Temperatura Mínima', 'Grados Celsius (°C)'), 'tmax':('Temepratura Máxima', 'Grados Celsius (°C)'), 'ws':('Rachas Máximas de Viento', 'km/h'), 'wd':('Dirección de Rachas Máximas de Viento', ), 'date':('Fecha', )}
        city = coll.Brief(location['url7'])
        url = city.urls[self.day]
        z_value = city.genArray(url, self.islast)
        coords = location['point']
        coords.insert(0, z_value[self.zindex])
        return {"attribute":coords, "date":z_value[6], "variable":variables[self.z][0], "units":variables[self.z][1]}

    def getAtts(self):
        """
        Get a dictionary with two elements.\n
            attsTable -> pandas.Dataframe object with the meteorological
        values and its respective coordinates pair (longitude,
        latitude) for every point within a shapefile.\n
            date -> Date data type (YYYY-MM-DD).
        """
        
        with ProcessPoolExecutor(max_workers=15) as exec:
            results = exec.map(self.getRec, urlCoords())
            atts = pd.DataFrame(columns=['z_value', 'lon', 'lat'])
            n = 1
            for result in results:
                atts.loc[len(atts)] = result['attribute']
                if n:
                    date = result['date']
                    variable = result['variable']
                    units = result['units']
                    n = 0
        return {"attsTable":atts, "date": date, 'variable': variable, "units": units}


class Mappers:
    """

    """

    def __init__(self, day, z):
        data = AttSeven(day, z).getAtts()
        self.attsTable = data['attsTable']
        self.date = data['date']
        self._title = f"Pronóstico Meteorológico para el día {self.date}\n{data['variable']}"
        self._units = data['units']
        

    def icubic(self):
        minVal = self.attsTable['z_value'].min()
        maxVal = self.attsTable['z_value'].max()
        imap = cp.m_MapInterpolation(shapefile_path=os.getenv(
            'state'), dataframe=self.attsTable, crs='epsg:4326')
        imap.draw(levels=np.arange(minVal, maxVal + 1, 0.1),
                  zoom_in=[(-102.2, -99.6), (19.87, 21.9)],
                  # show_points=True,
                  interpolation_method='cubic',
                  cbar_title='Temperatura Mínima (°C)',
                  title=f'Pronóstico para el día {self.date}',
                  title_ha='center',
                  title_x_position=0.5,
                  cmap='seismic',
                  save='map_Map.png'
                  )
    
    def toMap(self, method='kriging', save_path=None):
        if method != 'kriging':
            pass
        else:
            interData = interpol.Kriging(self.attsTable)
            interData.genMap(os.getenv('state'), bshp_path=os.getenv('bg'), title=self._title, save_path=save_path, labelBar=self._units)


if __name__ == '__main__':
    ini = Mappers(2, 'tmin')
    ini.toMap(save_path=r'C:\Users\Francisco Ruiz\Desktop\map_test.png')
    # ini.getAtts().to_csv('data.csv', index=False)
    
    # ini = AttSeven(2, 'tmin')
    # df = ini.getAtts()['attsTable']
    # df.to_csv('data20.csv')
