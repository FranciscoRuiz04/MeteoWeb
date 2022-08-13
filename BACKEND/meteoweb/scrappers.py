__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.2"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

########################    Packages    ########################

import requests
from bs4 import BeautifulSoup
#--------------------------------------------------------------#


########################    Classes    ########################

class Daily4cast:

    """

    Webscrapper to get information from meteoblue portal about the
    weather forecast for the current day and the next 6 days. Parameters
    like min and max temperatures, min and max precipitation, hours with
    sun, wind speed and direction, and forecast date are possible to get.


    Class object has the next initial attributes:\n

    self.url -> str type object with URL direction from which will be
    done the scrapping.\n
    self._class -> str type object with the tag class name used as
    reference to get the master content where is the predictions.\n
    self.tag -> bs4.element type object with the master content.\n

    IMPORTANT:\n
    To get the attributes self.date, self.temp, self.wind, self.precip,
    self.sun or self.prev is necessary to run either the functions date_fun(),
    tmp(), wind_fun(), precip_fun(), sunhrs() or previsibility() respectively
    one by one or solely predict() function.

    """

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
        (pmin, pmax) or (-999, -999)
        Outcome (-999, -999) appears when doesn't have rain forecast
        """

        val = self.tag.find(class_='tab-precip').text

        separators = ['<', '>', '-']
        for separator in separators:
            if separator in val:
                if separator == '-' or separator == '<':
                    values = val.split(separator)
                else:
                    values = list(reversed(val.split(separator)))
                    values[1] = int(values[0].replace('mm', '')) * 2
                break

        for n, value in enumerate(values):
            if value == '':
                values[n] = -999
            else:
                try:
                    values[n] = int(values[n].replace('mm', ''))
                except AttributeError:
                    pass

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

    """
    Daily4Cast object subclass to get information from meteoblue portal
    about the weather forecast for 6 days after the current date. Parameters
    like min and max temperatures, min and max precipitation, hours with
    sun, wind speed and direction, and forecast date are possible to get.


    Class object has the next initial attributes:\n

    self.url -> str type object with URL direction from which will be
    done the scrapping.\n
    self._class -> str type object with the tag class name used as
    reference to get the master content where is the predictions.\n
    self.tag -> bs4.element type object with the master content.\n

    IMPORTANT:\n
    To get the attributes self.date, self.temp, self.wind, self.precip,
    self.sun or self.prev is necessary to run either the functions date_fun(),
    tmp(), wind_fun(), precip_fun(), sunhrs() or previsibility() respectively
    one by one or solely predict() function.

    """

    def __init__(self, url, className="tab active last"):
        Daily4cast.__init__(self, url, className)


class H3ForeCast:

    """

    Webscrapper to get information from meteoblue portal about the
    weather forecast for the current day and the next 6 days every 3 hours.
    Parameters like min and max temperatures, min and max thermal sensation,
    and wind speed and direction are possible to get.


    Class object has the next initial attributes:\n

    self.url -> str type object with URL direction from which will be
    done the scrapping.\n
    self._class -> str type object with the tag class name used as
    reference to get the master content where is the predictions.\n
    self.tag -> bs4.element type object with the master content.\n

    IMPORTANT:\n
    To get the attributes self.temp, self.windS, self.windD, and self.tempF
    is necessary to run either the functions tmp(), windSpeed(), windDir() or
    one by one or solely predict() function.

    """

    def __init__(self, url, className="picto three-hourly-view"):
        Daily4cast.__init__(self, url, className)

    def __extractCells(dropfirst):
        def inner(fun):
            def wrap(self, **kargs):
                row = self.tag.find(class_=kargs['mainDiv'])
                wholeRecs = [div.text.strip()
                             for div in row.find_all(class_=kargs['chilDiv'])]
                if dropfirst:
                    wholeRecs.pop(0)
                else:
                    try:
                        curval = row.find(
                            class_=["cell no-mobile now"]).text.strip()
                        wholeRecs.insert(self.__ctime()[0], curval)
                    except AttributeError:
                        wholeRecs = [div.text.strip() for div in row.find_all(
                            class_=kargs['chilDiv'])]
                return fun(self, values=wholeRecs, **kargs)
            return wrap
        return inner

    def __ctime(self):
        lab = int(self.tag.find(class_='cell time now').text)//100
        hours = [3, 6, 9, 12, 15, 18, 21, 0]
        for i, hour in enumerate(hours):
            if lab == hour:
                return i, hour

    @__extractCells(dropfirst=True)
    def tmp(self, mainDiv, chilDiv, feeling=False, values=None):
        """

        Get the mean temperature in Celsius degrees.
        A list type object is the outcome with the next format:
        [val1, val2, ...]
        Every value is float type.

        Parameters:\n
        <mainDiv>
        Father tag classname where is the complete row inside
        the html table.
        <chilDiv>
        Child tag classname where is every table cell.
        <feeling>
        If True thermal sensation values will be get. By default
        is False.
        <Values>
        A list with the amounts only as str type objects.

        """
        outcome = list(map(lambda x: float(x[:-1]), values))
        if feeling:
            self.tempF = outcome
            return self.tempF
        else:
            self.temp = outcome
            return self.temp

    @__extractCells(dropfirst=False)
    def windSpeed(self, mainDiv, chilDiv, values=None):
        """

        Get the wind speed range in km/h.
        A dictionary type object is the outcome with the min and max values
        inside a list type object.
        The format is as follows:
        {"min":[val1, val2, ...], "max":[val1, val2, ...]}
        Both values are integers list.

        Parameters:\n
        <mainDiv>
        Father tag classname where is the complete row inside
        the html table.
        <chilDiv>
        Child tag classname where is every table cell.
        <Values>
        A list with the amounts only as str type objects.

        """
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
        self.windS = outcome
        return self.windS

    def windDirec(self, mainDiv):
        """

        Get the wind direction.
        A list type object is the outcome with the next format:
        ["Dir1", "Dir2", ...]
        Every list element is integer type.

        Parameters:\n
        <mainDiv>
        Father tag classname where is the complete row inside
        the html table.

        """
        row = self.tag.find(class_=mainDiv)
        wholedivs = row.find_all(class_='cell')
        divs = (wholediv.find('div') for wholediv in wholedivs)
        next(divs)
        outcome = [tag.text for tag in divs]
        self.windD = outcome
        return self.windD

    def predict(self):
        """

        Fetch all the variables considered by the class with just
        run this function.
        Variables will be saved in:
        self.temp = Temperature
        self.tempF = Thermal Sensation
        self.windS = Wind Speed
        self.windD = Wind Direction

        """

        self.windDirec(mainDiv='winddirs no-mobile')

        self.windSpeed(mainDiv='windspeeds', chilDiv='cell no-mobile')

        sameDiv = 'cell'
        self.tmp(mainDiv='temperatures', chilDiv=sameDiv)
        self.tmp(mainDiv='windchills', chilDiv=sameDiv, feeling=True)


class H1ForeCast:

    """

    Webscrapper to get information from meteoblue portal about the
    weather forecast for the current day and the next 6 days every hour.
    Parameters like precipitation probability and precipitation amout
    are possible to get.


    Class object has the next initial attributes:\n

    self.url -> str type object with URL direction from which will be
    done the scrapping.\n
    self._class -> str type object with the tag class name used as
    reference to get the master content where is the predictions.\n
    self.tag -> bs4.element type object with the master content.\n

    IMPORTANT:\n
    To get the attributes self.prob and self.mm is necessary to run
    either the functions probability() and millimeters() one by one
    or solely predict() function.

    """

    def __init__(self, url):
        H3ForeCast.__init__(self, url)

    def __completeDesc(function):
        def wrap(self, *kargs):
            ps = self.tag.find_all('p')
            l = [t.text.strip() for t in ps][:24]
            return function(self, cd=l)
        return wrap

    @__completeDesc
    def _time_fun(self, cd):
        """

        Get a list of lists with the considered hours for
        the forecast.

        Parameters:\n
        <cd>
        List type object with the complete description for every 
        forecasted hour.

        """
        timelist = []
        for hour in cd:
            hour.split('a')
            timelist.append(hour[:13])

        self.time = timelist
        return self.time

    @__completeDesc
    def probability(self, cd):
        """

        Get a list with the precipitation probability
        percentages.
        Every value is integer type.

        Parameters:\n
        <cd>
        List type object with the complete description for every 
        forecasted hour.

        """

        percents = []
        for desc in cd:
            percent = int(desc[14:].split('%')[0])
            percents.append(percent)

        self.proba = percents
        return self.proba

    @__completeDesc
    def millimeters(self, cd):
        """

        Get a list with the precipitation amounts in millimeters.
        Every value is float type.

        Parameters:\n
        <cd>
        List type object with the complete description for every 
        forecasted hour.

        """

        mms = []
        for desc in cd:
            descp = desc.split('.')[1]
            mm = float(descp.split()[0])
            mms.append(mm)

        self.mm = mms
        return self.mm

    def predict(self):
        """

        Fetch all the variables considered by the class with just
        run this function.
        Variables will be saved in:
        self.mm = Precipitation Amouts in mm
        self.proba = Precipitation Probability in %

        """

        self.millimeters()
        self.probability()


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv as env
    env()
    
    ini = H1ForeCast(os.getenv('starturl'))
    ini.predict()
    print(ini.probability())
    # ini.predict()
    # print(type(ini.temp))
    # for text in ini.info():
    #     print(text, end='\n\n')
    # ini.predict()
    # print(ini.proba, ini.mm)
    # print(ini.probability(), ini.millimeters(), sep='\n')
    # ini.predict()
    # print(ini.windS)
