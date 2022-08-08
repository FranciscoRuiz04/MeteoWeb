__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

########################    Packages    ########################

from sys import getsizeof
import requests
from bs4 import BeautifulSoup
# from dotenv import load_dotenv as env
#--------------------------------------------------------------#

# env()  # Get enviroment variables from .env file


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
            # self.html = _soup

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

        val = self.tag.find(class_='tab-precip').text

        separators = ['<', '>', '-']
        for separator in separators:
            if separator in val:
                if separator == '-' or separator == '<':
                    values = val.split(separator)
                else:
                    values = reversed(val.split(separator))
                break

        values = list(map(lambda x: x.strip(), values))

        for n, value in enumerate(values):
            if value == '':
                values[n] = None
            else:
                values[n] = int(values[n].replace('mm', ''))

        self.precip = tuple(values)

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


class H3ForeCast:

    def __init__(self, url, className="picto three-hourly-view"):
        Daily4cast.__init__(self, url, className)
        self.ws = None

    def __extractCells__(function):
        def wrap(self, **kargs):
            row = self.tag.find(class_=kargs['mainDiv'])
            wholeRecs = [div.text.strip()
                         for div in row.find_all(class_=kargs['chilDiv'])]
            wholeRecs.pop(0)
            return function(self, values=wholeRecs, **kargs)
        return wrap

    @__extractCells__
    def _tmps(self, mainDiv, chilDiv, feeling=False, values=None):
        outcome = list(map(lambda x: int(x[:-1]), values))
        if feeling:
            self.feeltmp = outcome
            return self.feeltmp
        else:
            self.tmp = outcome
            return self.tmp
    
    @__extractCells__
    def _windSpeed(self, mainDiv, chilDiv, values=None):
        pairs = (pair.split('-') for pair in values)
        values = ((int(value) for value in pair) for pair in pairs)
        vmin = []
        vmax = []
        for pair in values:
            vmin.append(next(pair))
            vmax.append(next(pair))
        
        outcome = {}
        outcome["min"] = vmin
        outcome["max"] = vmax
        self.ws = outcome
        return self.ws

    def _windDirec(self, mainDiv):
        row = self.tag.find(class_=mainDiv)
        wholedivs = row.find_all(class_='cell')
        divs = (wholediv.find('div') for wholediv in wholedivs)
        next(divs)
        outcome = [tag.text for tag in divs]
        self.wd = outcome
        return self.wd

    def predict(self):
        self._windDirec('winddirs no-mobile')
        self._windSpeed(mainDiv='windspeeds', chilDiv='cell no-mobile')
        
        sameDiv = 'cell'
        self._tmps(mainDiv='temperatures', chilDiv=sameDiv, feeling=True)
        self._tmps(mainDiv='windchills', chilDiv=sameDiv)



if __name__ == '__main__':
    # import os
    # ini = Daily4cast(
    #     os.getenv('starturl'), 'tab active last')
    # print(ini.tag)
    ini = H3ForeCast(r'https://www.meteoblue.com/es/tiempo/semana/san-miguel-de-allende_m%c3%a9xico_3985344')
    ini.predict()
    values = ini.ws
    print(values)
    
    