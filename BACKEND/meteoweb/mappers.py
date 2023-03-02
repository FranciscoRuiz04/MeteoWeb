__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


########################    Packages    ########################
from concurrent.futures import ThreadPoolExecutor
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
import cloupy as cp
import numpy as np
import pandas as pd
import os
import sys
from dotenv import load_dotenv as env
env()

#-----------------------    GPS Pckgs    ----------------------#
# To developing
import collectors as coll
import interpolation_methods as interpol

# To exec file creation
# from . import collectors as coll
# from . import interpolation_methods as interpol


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
        
        variables = {'pp':('Probabilidad de Precipitación', '%'), 'p':('Precipitación', 'Milímetros de lluvia (mm)'), 'tmin':('Temperatura Mínima', 'Grados Celsius (°C)'), 'tmax':('Temperatura Máxima', 'Grados Celsius (°C)'), 'ws':('Rachas Máximas de Viento', 'km/h'), 'wd':('Dirección de Rachas Máximas de Viento', ), 'date':('Fecha', )}
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
        try:
            with ThreadPoolExecutor(max_workers=15) as exec:
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
        except:
            return None
        else:
            return {"attsTable":atts, "date": date, 'variable': variable, "units": units}


class Mappers:
    """

    """

    def __init__(self, day, z):
        data = AttSeven(day, z).getAtts()
        
        assert data != None, 'Empty Arrangement'
        
        self.data = data['attsTable']
        self.date = data['date']
        self._title = f"Pronóstico Meteorológico para el día {self.date}\n{data['variable']}"
        self._units = data['units']
        self.interpolationMethods = dict(OK=interpol.OK, UK=interpol.UK, IDW=None)
        
        # Data vectors
        self.lons = lons = np.array(self.data['lon'])
        self.lats = lats = np.array(self.data['lat'])
        self.z_values = np.array(self.data['z_value'])
        
        # Grid configuration
        # Longitude interval
        xmin_grid = np.amin(lons)
        xmax_grid = np.amax(lons)
        self.grid_lon = np.arange(xmin_grid, xmax_grid, 0.01)
        # Latitude interval
        ymin_grid = np.amin(lats)
        ymax_grid = np.amax(lats)
        self.grid_lat = np.arange(ymin_grid, ymax_grid, 0.01)


    def spline(self, save_path, shp_path=None, **kargs):
        
        minVal = self.z_values.min()
        maxVal = self.z_values.max()
        
        if 'crs' not in kargs.keys():
            kargs['crs'] = 'epsg:4326'
        if shp_path == None:
            shp_path=os.getenv('state')
        
        # Mapping Process
        imap = cp.m_MapInterpolation(shapefile_path=shp_path, dataframe=self.data, **kargs)
        imap.draw(levels=np.arange(minVal, maxVal + 1, 0.1),
                  zoom_in=[(-102.2, -99.6), (19.87, 21.9)],
                  interpolation_method='cubic',
                  cbar_title=self._units,
                  title=self._title,
                  title_ha='center',
                  title_x_position=0.5,
                  cmap='seismic',
                  save=save_path
                  )
    
    
    def chooseMethod(self,  method, shp_path=None, saveList=None, cramp='seismic', shp_contour_col='black', bshp_path=None, save_path=None, ncontours=None, bshp_contour_col=None):
        
        # Prevent 0 vector. If there is a forecast equal to zero
        # for every station won't execute none interpolation method.
        if sum(self.z_values) == 0:
            return None
        
        else:
            if 'K' in method:
                # Inteprolation Process
                interpolClass = self.interpolationMethods[method]
                methodInstance = interpolClass(self.lons, self.lats, self.z_values)
                interpolatedValues, _ = methodInstance.interpolateValues(self.grid_lon, self.grid_lat)
            
            
                # Basemap Creation
                if shp_path == None:
                    shp_path = os.getenv('state')
                shp = gpd.read_file(shp_path)
                xintrp, yintrp = np.meshgrid(self.grid_lon, self.grid_lat)    # Generate a meshgrid
                fig, ax = plt.subplots()    # ax is the plot base area. Multi-plotting.
                
                
                if ncontours == None:
                    ncontours = len(interpolatedValues)
                contour = plt.contourf(xintrp, yintrp, interpolatedValues, ncontours, cmap=mpl.colormaps[cramp])  # Fourth argument represents contours number
                shp.plot(ax = ax, color = shp_contour_col)
                
                # Plotting state bound and display components
                if bshp_path == None:
                    bshp = gpd.read_file(os.getenv('bg'))
                if bshp_contour_col == None:
                    bshp_contour_col = 'black'
                bshp.plot(ax = ax, color = bshp_contour_col, linewidth = 0.5)
                
                
                # Styling the map
                minVal = round(np.amin(interpolatedValues))
                maxVal = round(np.amax(interpolatedValues))    
                
                plt.colorbar(contour, label= self._units, ticks=range(minVal, maxVal + 1, 2))
                plt.clim(minVal, maxVal)
                plt.xlabel('Longitud', fontsize=10)
                plt.ylabel('Latitud', fontsize=10)
                plt.xticks(fontsize=9)
                plt.yticks(fontsize=9, ticks=[20, 20.5, 21, 21.5], labels=[20.0, 20.5, 21.0, 20.5])
                plt.annotate('Fuente: meteoblue.com. Mapa Base: Marco Geoestadístico 2020. INEGI. EPSG:4326', ha='left', va='center', xy=(0,-.15), xycoords='axes fraction', fontsize=7)
                plt.title(self._title, fontsize=11, ha='center')
                
                # Zoom in to wanted area
                plt.axis([np.amin(xintrp), np.amax(xintrp), np.amin(yintrp), np.amax(yintrp)])
                
                
                # Save image only
                if save_path == None and saveList == None:
                    plt.show()
                
                elif saveList != None:
                    try:
                        init_stout = sys.stdout
                        with open(saveList[1], 'w') as myfile:
                            sys.stdout = myfile
                            methodInstance.print_statistics()
                        plt.savefig(saveList[0], dpi=300, bbox_inches='tight')
                    except:
                        print('Has occured an error. Both files png and txt have not been created.')
                    finally:
                        sys.stdout = init_stout
                
                else:
                    try:
                        components = os.path.splitext(save_path)
                        save_path = components[0] + '.png'
                    except:
                        save_path += '.png'
                    plt.savefig(save_path, dpi=300, bbox_inches='tight')









if __name__ == '__main__':
    # import pandas as pd
    ini = Mappers(2, 'tmin')
    # print(ini.z_values)
    ini.chooseMethod('UK', saveList=[r'C:/Users/Francisco Ruiz/Desktop/mw/UK.png', r'C:/Users/Francisco Ruiz/Desktop/mw/UK.txt'])
    # ini.getAtts().to_csv('data.csv', index=False)
    # ini = AttSeven(2, 'tmin')
    # df = ini.getAtts()['attsTable']
    # df.to_csv('data20.csv')
