import sys
import os
from tkinter import messagebox as ms
from dotenv import load_dotenv as env
sys.path[0] = sys.path[0][:-8]
from BACKEND import logic

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
            name = False
        else:
            cityname = name.lower().replace(' ', '-')
        try:
            cond = logic.newPlace(root=os.getenv('root'), url=inurl,
                                  targetpath=folder, cityname=cityname)
            if cond == None:
                ms.showinfo(title="New city added",
                            message=f"{name} HAS ADDED AS {cityname}!")
            else:
                ms.showinfo(title="City Duplicity",
                            message=f"{name} already exists")
        except:
            ms.showerror(title="Error", message="Has occured an error")
    else:
        ms.showwarning(title="Not filled field",
                       message="One or more fields are empty. Complete it.")

def brief():
    for i in logic.getPlaces(os.getenv('root')):
        url = i["url"].split('.com')[-1]
        yield [i["city"], i["path"], url]