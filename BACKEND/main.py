__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.2"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


########################    Packages    ########################

import os, sys
from dotenv import load_dotenv as env
sys.path.append(os.getenv('BACKENDMods'))
from concurrent.futures import ThreadPoolExecutor
#-----------------------    GPS Pckgs    ----------------------#

import logic
from meteoweb import creators
#--------------------------------------------------------------#
env()

def run(place):
    obj1 = creators.File_24H(place, 'txt', 'utf-8')
    obj2 = creators.File_3H(place, 'txt', 'utf-8')
    obj3 = creators.File_1H(place, 'txt', 'utf-8')
    
    obj1.NewFile()
    obj2.NewFile()
    obj3.NewFile()


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
                exec.map(run, places)
        except:
            raise ValueError("Some value is wrong")
#--------------------------------------------------------------#

# exec()

#--------------------------------------------------------------#
