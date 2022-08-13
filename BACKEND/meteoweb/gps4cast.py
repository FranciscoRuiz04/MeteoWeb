__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.2"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

########################    Packages    ########################
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
from concurrent.futures import ThreadPoolExecutor
#-----------------------    GPS Pckgs    ----------------------#
from . import scrappers as mw
# import scrappers as mw
#--------------------------------------------------------------#



########################    Functions    ########################


def decorator(function):
    def tab4cast(url, factor):
        """
        Generate a list with the values fetched from web page
        """

        try:
            data = function(url, factor)
            data.predict()
        except:
            dfr = [None for _ in range(9)]
        else:
            if factor == 3:
                dfr = {"Temp": data.temp, "TermSens": data.tempF,
                       "WSpeed_Min": data.windS["min"], "WSpeed_Max": data.windS["max"], "WDir": data.windD}
            elif factor == 1:
                dfr = {"Probability(%)":data.proba, "Precipitation(mm)":data.mm}
            else:
                dfr = [data.date, data.temp[0], data.temp[1],
                       data.wind[0], data.wind[1], data.precip[0], data.precip[1], data.sun, data.prev]
        return dfr
    return tab4cast


@decorator
def normTab(url, factor):
    """

    Extract xml format content from 6 firsts days forecast
    within <<tab>> tag
    """

    data2 = mw.Daily4cast(url)
    return data2


@decorator
def lastTab(url, factor):
    """

    Extract xml format content from last day forecast
    within <<tab>> tag
    """
    data2 = mw.Last4cast(url)
    return data2


@decorator
def h3tab(url, factor):
    data2 = mw.H3ForeCast(url)
    return data2


@decorator
def h1tab(url, factor):
    data2 = mw.H1ForeCast(url)
    return data2

########################    Generators    ########################


def _genLinks(item):
    for i in item:
        links = i.find('a')
        path = links.get('href')
        if path and path.startswith('/'):
            path = os.getenv('mainurl') + path
        yield path


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
# import logging
# logging.basicConfig(level=logging.DEBUG, format='%(threadName)s:%(message)s')


def run(mainurl, factor=None):
    """
    Extract a dataframe type object with all the information about
    daily forecast ordered by date, using multiple-threads with
    threadpool.
    """

    urls = get_linked_urls(mainurl)
    with ThreadPoolExecutor(max_workers=4) as exec:
        if factor is None:
            outcome = dailyDF(exec, urls, factor)
        elif factor == 3:
            outcome = h3DF(exec, urls, factor)
        else:
            outcome = h1DF(exec, urls, factor)
        
        return outcome


def h3DF(exec_obj, urls, factor):
    results = exec_obj.map(h3tab, urls, [factor]*7)
    
    dfs = []
    for result in results:
        df = pd.DataFrame(result)
        dfs.append(df)
    
    return dfs


def h1DF(exec_obj, urls, factor):
    results = exec_obj.map(h1tab, urls, [factor]*7)
    
    dfs = []
    for result in results:
        df = pd.DataFrame(result)
        dfs.append(df)
    
    return dfs


def dailyDF(exec_obj, urls, factor):
    results = exec_obj.map(normTab, urls[:-1], [factor]*6)
    last = exec_obj.submit(lastTab, urls[-1], factor).result()

    recs = []
    for result in results:
        recs.append(result)
    recs.append(last)

    df = pd.DataFrame(data=recs, columns=[
                      "Date", "Tmin(°C)", "Tmax(°C)", "WSpeed(km/h)", "WDirec", "Pmin(mm)", "Pmax(mm)", "Sun(hrs)", "Prev"])
    # df.sort_values(by='Date', ascending=True)

    return df
#--------------------------------------------------------------#


if __name__ == '__main__':
    import os
    from dotenv import load_dotenv as env
    env()
    # for i,df in enumerate(run(os.getenv('starturl'), 3)):
    #     print(df, i, sep='/'*5, end='\n\n')
    print(run(os.getenv('starturl'), 3))
