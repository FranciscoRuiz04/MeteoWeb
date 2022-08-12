__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.2"
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
        filepath = os.listdir(pathfolder)[-1]
    except IndexError as e:
        print(e)

    else:
        oldFile = pd.read_csv(pathfolder + os.sep + filepath, encoding='utf-8')

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
    content1H = gps4cast.run(mainurl, 1)
    content3H = gps4cast.run(mainurl, 3)

    creation = datetime.now().strftime("%d%m%y_%H%M")
    day = creation.split('_')[0]
    time = creation.split('_')[1]

    name = cityname + '_C' + creation
    filename = name + '.' + format

    folders = ['1H', '3H', '24H']
    for fder in folders:
        childfolder = folder + os.sep + fder

        try:
            if fder == '24H':
                forfile24H(content, filename, childfolder, day)
            elif fder == '1H':
                forfiles1H_3H(content1H, filename, childfolder, day, time)
            else:
                forfiles1H_3H(content3H, filename, childfolder, day, time)
        except:
            raise RuntimeError(
                "Somthing was wrong. Maybe files were not been created")


def forfile24H(data, filename, mainfolder, day):
    folder = mainfolder + os.sep + day
    filepath = folder + os.sep + filename

    if not os.path.exists(folder):
        os.makedirs(folder)
        data.to_csv(filepath, encoding='utf-8', index=False)
    else:
        if len(os.listdir(folder)) > 0 and not isredundant(data, folder):
            data.to_csv(filepath, encoding='utf-8', index=False)


def forfiles1H_3H(data, filename, mainfolder, day, time):
    pathcomponents = [mainfolder, day, time]
    filefolder = os.sep.join(pathcomponents)
    if not os.path.exists(filefolder):
        os.makedirs(filefolder)

    n = int(day[:2])
    for df in data:
        filepath = filefolder + os.sep + str(n) + '_' + filename
        df.to_csv(filepath, encoding='utf-8', index=False)
        n += 1


def runAlgorithm(place):
    targetPath = place["path"]
    url = place["url"]
    name = place["city"]

    return toFile(targetPath, url, name)
