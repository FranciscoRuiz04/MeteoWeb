########################    Packages    ########################
import os
from shutil import ExecError
import pandas as pd
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
#-----------------------    GPS Pckgs    ----------------------#
from . import scrappers as scr
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


def get_linked_urls(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')
    labels = (label for label in soup.find_all(class_='tab'))
    links = _genLinks(labels)
    urls = []
    for link in links:
        urls.append(link)
    return urls




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
    
    def today(self):
        firstlink = self.url
        first = self.__genDailyrow(firstlink)
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
    
    def firstDay(self, url, dataframe=True):
        try:
            data = scr.H3ForeCast(url)
            data.predict()
        except:
            raise ExecError("Prediction has not been executed")
        else:
            content = {"Temp": data.temp, "TermSens": data.tempF,
                    "WSpeed_Min": data.windS["min"], "WSpeed_Max": data.windS["max"],
                    "WDir": data.windD}
            
            if dataframe: outcome = pd.DataFrame(content)
            else: outcome = content
            
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
            content = {"Probability(%)":data.proba, "Precipitation(mm)":data.mm}
            
            if dataframe:
                outcome = pd.DataFrame(content)
            else:
                outcome = content
            
            return outcome


if __name__=='__main__':
    import os
    from dotenv import load_dotenv as env
    env()
    ini = H1Array(os.getenv('starturl'))
    print(ini.genArray())