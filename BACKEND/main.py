########################    Packages    ########################

from datetime import datetime
import os
from meteoweb import gps4cast
# from dotenv import load_dotenv as env
import logic
from concurrent.futures import ThreadPoolExecutor
#--------------------------------------------------------------#
# env()  # Get enviroment variables

########################    Functions    ########################


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


def fun(place):
    targetPath = place["path"]
    url = place["url"]
    name = place["city"]
    toFile(targetPath, url, name)


########################    Exexution    ########################
try:
    # Get place properties for every object in JSON file
    places = logic.getPlaces(os.getenv('root'))
except:
    raise FileExistsError("DB file does not exist")
else:
    try:
        # Generate files with determined properties
        with ThreadPoolExecutor(max_workers=2) as exec:
            exec.map(fun, places)
    except:
        raise ValueError("Some value is wrong")
