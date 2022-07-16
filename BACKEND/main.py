########################    Packages    ########################

from datetime import datetime
import os
from meteoweb import gps4cast
from dotenv import load_dotenv as env
import logic
#--------------------------------------------------------------#

env()  # Get enviroment variables

places = logic.getPlaces(os.getenv('root'))  # Get place file properties

########################    Classes    ########################


def toFile(path, mainurl, cityname, format='txt'):
    """
    Create a file with the daily forecast for a particular place
    using its url.
    Outcome file is named with its cityname followed by its creation
    date and time
    """

    content = gps4cast.run(mainurl)
    creation = datetime.now().strftime("%b-%d-%Y_%H-%M")
    name = cityname + '_' + creation
    file = path + os.sep + name + '.' + format
    content.to_csv(file, encoding='utf-8', index=False)


# Generate files with determined properties
for place in places:
    targetPath = place["path"]
    url = place["url"]
    name = place["city"]
    toFile(path=targetPath, mainurl=url, cityname=name)

# toFile(r"C:/DailyForecast_test", "https://www.meteoblue.com/es/tiempo/semana/guanajuato_m%c3%a9xico_4005270",'guanas')
