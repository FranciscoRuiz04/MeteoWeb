__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "2.0.0"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

########################    Packages    ########################

import os
from shutil import ExecError
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
#-----------------------    GPS Pckgs    ----------------------#
# Module importation to exec file creation and distribution
# from . import scrappers as scr

# Module importation to be developing
import scrappers as scr
#--------------------------------------------------------------#


########################    Generators    ########################
def _genLinks(item):
    for i in item:
        links = i.find('a')
        path = links.get('href')
        if path and path.startswith('/'):
            path = os.getenv('mainurl') + path
        yield path
#--------------------------------------------------------------#

########################    Function    ########################


def get_linked_urls(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    labels = (label for label in soup.find_all(class_='tab'))
    links = _genLinks(labels)
    urls = []
    for link in links:
        urls.append(link)
    return urls
#--------------------------------------------------------------#


class ForeteenArray:

    def __init__(self, url):
        self.url = url

    def data(self):
        try:
            data = scr.ForeteenCast(self.url)
            data.predict()
        except:
            dfr = [-999 for _ in range(15)]
        else:
            dfr = [data.precip['mm'], data.precip['mm_sd'], data.precip['proba'],
                   data.temp['min'], data.temp['max'], data.date]
        finally:
            return dfr

    def genArray(self, dataframe=True):
        try:
            data = scr.ForeteenCast(self.url)
            data.predict()
        except:
            return None
        else:
            if dataframe:
                df = pd.DataFrame()
                df['mm'] = data.precip['mm']
                df['sd'] = data.precip['mm_sd']
                df['%'] = data.precip['proba']
                df['°C_Min'] = data.temp['min']
                df['°C_Max'] = data.temp['max']
                df['Date'] = data.date
            else:
                df = self.data()
            return df


class DailyArray:

    def __init__(self, url):
        self.url = url
        self.urls = get_linked_urls(self.url)

    def __genDailyrow(self, url, lastday=False):
        try:
            if lastday:
                data = scr.Last4cast(url)
            else:
                data = scr.Daily4cast(url)
            data.predict()
        except:
            dfr = [None for _ in range(9)]
        else:
            dfr = [data.date, data.temp[0], data.temp[1],
                   data.wind[0], data.wind[1], data.precip[0],
                   data.precip[1], data.sun, data.prev]
        finally:
            return dfr

    def today(self, url, last=False):
        firstlink = url
        first = self.__genDailyrow(firstlink, last)
        return first

    def sixFirstDays(self):
        links = self.urls
        with ThreadPoolExecutor(max_workers=4) as exec:
            results = exec.map(self.__genDailyrow, links[:-1])
            recs = []
            for result in results:
                recs.append(result)
        return recs

    def lastDay(self):
        lastlink = self.urls[-1]
        last = self.__genDailyrow(lastlink, True)
        return last

    def genArray(self, dataframe=True):
        fullcontent = self.sixFirstDays()
        lastday = self.lastDay()
        fullcontent.append(lastday)

        if dataframe:
            outcome = pd.DataFrame(data=fullcontent, columns=[
                "Date", "Tmin(°C)", "Tmax(°C)",
                "WSpeed(km/h)", "WDirec", "Pmin(mm)",
                "Pmax(mm)", "Sun(hrs)", "Prev"])
        else:
            outcome = fullcontent

        return outcome


class H3Array:

    def __init__(self, url):
        DailyArray.__init__(self, url)

    def rain(self, url):
        data = scr.H1ForeCast(url)
        data.predict()
        i = 0
        for _ in range(8):
            s = 0
            probaRange = data.proba[i:i+3]
            for val in data.mm[i:i+3]:
                s += val
                i += 1
            yield s, max(probaRange)

    def firstDay(self, url, dataframe=True):
        try:
            data = scr.H3ForeCast(url)
            data.predict()
        except:
            raise ExecError("Prediction has not been executed")
        else:
            rainInfo = [t for t in self.rain(url)]
            content = {"%": [v[1] for v in rainInfo], "mm": [v[0] for v in rainInfo], "Temp": data.temp, "TermSens": data.tempF,
                       "WSpeed_Min": data.windS["min"], "WSpeed_Max": data.windS["max"],
                       "WDir": data.windD}

            if dataframe:
                outcome = pd.DataFrame(content)
            else:
                outcome = content

            return outcome

    def genArray(self):
        dflist = []
        for url in self.urls:
            info = self.firstDay(url)
            dflist.append(info)
        return dflist


class H1Array(H3Array):

    def __init__(self, url):
        super().__init__(url)

    def firstDay(self, url, dataframe=True):
        try:
            data = scr.H1ForeCast(url)
            data.predict()
        except:
            raise ExecError("Prediction has not been executed")
        else:
            content = {"Probability(%)": data.proba,
                       "Precipitation(mm)": data.mm}

            if dataframe:
                outcome = pd.DataFrame(content)
            else:
                outcome = content

            return outcome


class Brief(DailyArray):

    def __init__(self, url):
        DailyArray.__init__(self, url)

    def baseArray(self, url, last=False):
        supdata = DailyArray.today(self, url, last)
        data = supdata[1:5]
        data.append(supdata[0])
        return data

    def precipitation(self, url):
        df = H1Array.firstDay(self, url)
        percent = df["Probability(%)"].max()
        accumrain = df["Precipitation(mm)"].sum()
        pair = [percent, accumrain]
        return pair

    def genArray(self, url, last=False):
        with ThreadPoolExecutor(max_workers=2) as exec:
            pdata = exec.submit(self.precipitation, url).result()
            restdata = exec.submit(self.baseArray, url, last).result()
        fulldata = pdata + restdata
        return fulldata


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv as env
    env()
    ini = ForeteenArray(os.getenv('starturl'))
    print(ini.genArray())
