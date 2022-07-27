__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


########################    Packages    ########################

import os
# from dotenv import load_dotenv as env
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.blocking import BlockingScheduler
#-----------------------    GPS Pckgs    ----------------------#

import logic
import index
#--------------------------------------------------------------#


########################    Execution    ########################
def exec():
    try:
        # Get place properties for every object in JSON file
        places = logic.getPlaces(os.getenv('root'))
    except:
        raise FileExistsError("DB file does not exist")
    else:
        try:
            # Generate files with determined properties
            with ThreadPoolExecutor(max_workers=2) as exec:
                exec.map(index.fun, places)
        except:
            raise ValueError("Some value is wrong")
    finally:
        print('Algorithm runned')
        
exec()
########################    Schedule    ########################
scheduler = BlockingScheduler()
scheduler.add_job(exec, 'interval', hours=1)
scheduler.start()
