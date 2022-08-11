__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


########################    Packages    ########################

from datetime import datetime
import os
# from dotenv import load_dotenv as env
import pandas as pd
#--------------------------------------------------------------#
# env()  # Get enviroment variables
from meteoweb import gps4cast

########################    Functions    ########################


def isredundant(dfObj, pathfolder):

    try:
        file = os.listdir(pathfolder)[-1]
    except IndexError as e:
        print(e)

    else:
        oldFile = pd.read_csv(pathfolder + os.sep + file, encoding='utf-8')

        for n, row in dfObj.iterrows():

            newRow = list(map(str, list(row)))
            oldRow = list(map(str, list(oldFile.iloc[n])))

            if newRow != oldRow:
                return False

        return True


def toFile(folder, mainurl, cityname, format='txt'):
    """
    Create a file with the daily forecast for a particular place
    using its url.
    Outcome file is named with its cityname followed by its creation
    date and time
    """

    content = gps4cast.run(mainurl)

    creation = datetime.now().strftime("%b-%d-%Y_%H-%M")
    name = cityname + '_' + creation
    file = folder + os.sep + name + '.' + format

    if not os.path.isdir(folder):
        os.makedirs(folder)
        content.to_csv(file, encoding='utf-8', index=False)

    else:
        if len(os.listdir(folder)) > 0 and not isredundant(content, folder):
            content.to_csv(file, encoding='utf-8', index=False)


def fun(place):
    targetPath = place["path"]
    url = place["url"]
    name = place["city"]

    return toFile(targetPath, url, name)
