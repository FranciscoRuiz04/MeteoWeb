########################    Packages    ########################
import pandas as pd
import requests
from bs4 import BeautifulSoup
from . import meteoweb as mw
# from dotenv import load_dotenv as env
import os
from concurrent.futures import ThreadPoolExecutor
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
    for link in links:
        yield link
#--------------------------------------------------------------#


def run(mainurl):
    """
    Extract a dataframe type object with all the information about
    daily forecast ordered by date, using multiple-threads with
    threadpool.
    """

    recs = []
    with ThreadPoolExecutor(max_workers=3) as exec:
        for n, url in enumerate(get_linked_urls(mainurl)):
            if n == 6:
                result = exec.submit(lastTab, url).result()
            else:
                result = exec.submit(normTab, url).result()
            recs.append(result)
    df = pd.DataFrame(data=recs, columns=[
                      "Date", "Tmin(°C)", "Tmax(°C)", "WSpeed(km/h)", "WDirec", "Pmin(mm)", "Pmax(mm)", "Sun(hrs)", "Prev"])
    df.sort_values(by='Date', ascending=True)
    return df
#--------------------------------------------------------------#


if __name__ == '__main__':
    print(run(os.getenv('starturl')))