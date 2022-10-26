########################    Packages    ########################

import matplotlib.pyplot as plt
import geopandas as geopd
import pandas as pd
import os
#-----------------------    GPS Pckgs    ----------------------#
# Module importation to exec file creation
# from . import collectors
# from . import scrappers as scr

# Module importation to be developing
import scrappers as scr
import collectors
#--------------------------------------------------------------#


class Attribute(collectors.Brief):

    def __init__(self, url):
        super().__init__(url)
        self.coords = scr.Daily4cast(url).coords

    def baseArray(self, url, last=False):
        fulldata = super().baseArray(url, last)
        outcome = fulldata[:2]
        return outcome

    def genArray(self, url, last=False):
        parameters = super().genArray(url, last)
        row = parameters[1:] + self.coords
        names = ['Accum_P', 'Tmp_Min', 'Tmp_Max', 'Lat', 'Lon', 'Elev']
        outcome = {names[n]: value for n, value in enumerate(row)}
        return outcome


class AttributesTable:

    def __init__(self, attObj, genObj):
        self.__genObj = genObj(os.getenv('root'))
        self.__attObj = attObj

    def records(self):
        for loc in self.__genObj:
            obj = self.__attObj(loc['url'])
            record = obj.genArray(loc['url'])
            record['Loc'] = loc['city']
            yield record

    def genTable(self, export=False):
        atts = pd.DataFrame()
        for att in self.records():
            atts = atts.append(att, ignore_index=True)
        attTable = geopd.GeoDataFrame(atts,
                                      geometry=geopd.points_from_xy(atts['Lon'],
                                                                    atts['Lat'],
                                                                    atts['Elev']))
        if export:
            attTable.to_file('C:\DailyForecast_test\muns_wgs84.shp', driver='ESRI Shapefile')
        else:
            return attTable

    def mapping(self):
        attTable = self.genTable()
        attTable.plot()
        plt.show()

if __name__ == '__main__':
    import sys
    from dotenv import load_dotenv as env
    env()
    sys.path.append(os.getenv('BACKENDMods'))
    import logic
    
    ini = AttributesTable(attObj=Attribute, genObj=logic.getPlaces)
    ini.genTable(True)