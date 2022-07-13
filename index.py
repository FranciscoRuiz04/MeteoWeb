import pandas as pd
import gps4cast as fc
from dotenv import load_dotenv as env
import os
import concurrent.futures

env()

_main = os.getenv('starturl')
_urls = fc.get_linked_urls(_main)


def tab4cast(url, df, index=0):
    try:
        data = fc.DailyForecast(url)
        data.predict()
    except:
        dfr = [None for _ in range(7)]
    else:
        wspeed = str(data.wind[0]) + ' ' + str(data.wind[1])
        p = str(data.precip[0]) + ' - ' + str(data.precip[1])
        df.loc[index] = [data.date, data.temp[0], data.temp[1],
                         wspeed, p, data.sun, data.prev]
        # dfr = [data.date, data.temp[0], data.temp[1],
        #     wspeed, p, data.sun, data.prev]
    return dfr

# mydf = pd.DataFrame(columns=["Date", "Tmin", "Tmax", "WSpeed", "Precip", "Sun", "Prev"])



if __name__ == '__main__':
    ini = tab4cast(_main)