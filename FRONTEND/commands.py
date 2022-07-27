__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

########################    Packages    ########################
import sys
import os
from tkinter import messagebox as ms
from dotenv import load_dotenv as env
sys.path[0] = sys.path[0][:-8]
#-----------------------    GPS Pckgs    ----------------------#
from BACKEND import logic
#--------------------------------------------------------------#

env()


def dropCommand(inp):
    if inp != '':
        entry = inp.lower()
        try:
            if logic.dropPlace(root=os.getenv('root'), cityname=entry):
                ms.showinfo(title="City Dropped", message=f"{inp} HAS DROPPED!")
            else:
                ms.showinfo(title="No element", message="No element matched")
        except:
            ms.showinfo(title="Exist Error", message="Has occured an error")
    else:
        ms.showerror(title="No value", message="Entry a valid value")


def addCommand(inurl, folder, name):
    if inurl != '' and folder != '':
        if name == '':
            city = False
        else:
            city = name.lower().replace(' ', '-')
        try:
            cityname = logic.newPlace(root=os.getenv('root'), url=inurl,
                                  targetpath=folder, cityname=city)
            if cityname[0]:
                ms.showinfo(title="New city added",
                            message=f"{name} HAS ADDED AS {cityname[1]}!")
            else:
                ms.showinfo(title="City Duplicity",
                            message=f"{cityname[1]} already exists")
        except:
            ms.showerror(title="Error", message="Has occured an error")
    else:
        ms.showwarning(title="Not filled field",
                       message="One or more fields are empty. Complete it.")

def brief():
    for i in logic.getPlaces(os.getenv('root')):
        url = i["url"].split('.com')[-1]
        yield [i["city"], i["path"], url]

if __name__=='__main__':
    addCommand("https://www.meteoblue.com/es/tiempo/semana/guadalajara_m%c3%a9xico_4005539", "C:\DailyForecast_test", '')
