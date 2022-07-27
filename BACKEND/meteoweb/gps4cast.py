__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

########################    Packages    ########################
import pandas as pd
import requests
from bs4 import BeautifulSoup
# from dotenv import load_dotenv as env
import os
from concurrent.futures import ThreadPoolExecutor
#-----------------------    GPS Pckgs    ----------------------#
from . import meteoweb as mw
# import meteoweb as mw

#--------------------------------------------------------------#


# env()  # Get constant values from .env file


########################    Functions    ########################


def decorator(function):
    def tab4cast(url):
        """
        Generate a list with the values fetched from web page
        """

        try:
            data = function(url)
            data.predict()
        except:
            dfr = [None for _ in range(7)]
        else:
            # data.wind = str(data.wind[0]) + ' ' + str(data.wind[1])
            # data.precip = str(data.precip[0]) + ' - ' + str(data.precip[1])
            dfr = [data.date, data.temp[0], data.temp[1],
                   data.wind[0], data.wind[1], data.precip[0], data.precip[1], data.sun, data.prev]
        return dfr
    return tab4cast


@decorator
def normTab(url):
    """

    Extract xml format content from 6 firsts days forecast
    within <<tab>> tag
    """

    data = mw.Daily4cast(url)
    return data


@decorator
def lastTab(url):
    """

    Extract xml format content from last day forecast
    within <<tab>> tag
    """

    data = mw.Last4cast(url)
    return data


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

def run(mainurl):
    """
    Extract a dataframe type object with all the information about
    daily forecast ordered by date, using multiple-threads with
    threadpool.
    """

    recs = []
    urls = get_linked_urls(mainurl)
    with ThreadPoolExecutor(max_workers=4) as exec:
        results = exec.map(normTab, urls[:-1])
        last = exec.submit(lastTab, urls[-1]).result()
    for result in results:
        recs.append(result)
    recs.append(last)

    df = pd.DataFrame(data=recs, columns=[
                      "Date", "Tmin(°C)", "Tmax(°C)", "WSpeed(km/h)", "WDirec", "Pmin(mm)", "Pmax(mm)", "Sun(hrs)", "Prev"])
    df.sort_values(by='Date', ascending=True)
    return df
#--------------------------------------------------------------#


if __name__ == '__main__':
    print(run(os.getenv('starturl')))
