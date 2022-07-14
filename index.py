import pandas as pd
import gps4cast as fc
from dotenv import load_dotenv as env
import os
from concurrent.futures import ThreadPoolExecutor

env()

_main = os.getenv('starturl')
_urls = fc.get_linked_urls(_main)


def decorator(function):
    def tab4cast(url):
        try:
            data = function(url)
            data.predict()
        except:
            dfr = [None for _ in range(7)]
        else:
            wspeed = str(data.wind[0]) + ' ' + str(data.wind[1])
            p = str(data.precip[0]) + ' - ' + str(data.precip[1])
            dfr = [data.date, data.temp[0], data.temp[1],
                   wspeed, p, data.sun, data.prev]
        return dfr
    return tab4cast


@decorator
def normTab(url):
    data = fc.Daily4cast(url)
    return data


@decorator
def lastTab(url):
    data = fc.Last4cast(url)
    return data


def run():
    recs = []
    with ThreadPoolExecutor(max_workers=3) as exec:
        for n, url in enumerate(_urls):
            if n == 6:
                result = exec.submit(lastTab, url).result()
            else:
                result = exec.submit(normTab, url).result()
            recs.append(result)
    df = pd.DataFrame(data=recs, columns=[
                      "Date", "Tmin", "Tmax", "WSpeed", "Precip", "Sun", "Prev"])
    df.sort_values(by='Date', ascending=True)
    return df


if __name__ == '__main__':
    print(run())
