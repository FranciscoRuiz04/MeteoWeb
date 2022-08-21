
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
from threading import Thread
from dotenv import load_dotenv as env
import tkinter as tk
sys.path[0] = sys.path[0][:-8]
#-----------------------    GPS Pckgs    ----------------------#
## Module importation to exec file creation
from . import widgets as wdg
## Module importation to be developing
# import widgets as wdg
from BACKEND import logic
from BACKEND import summation
#--------------------------------------------------------------#

env()

def __myfun():
    global out
    out = summation.exec(logic.getPlaces(os.getenv('root')))
    

def summarize(root):
    try:
        t = Thread(target=__myfun, daemon=True)
        t.start()
        loading = tk.Toplevel(root)
        loading.title('Running Process')
        # loading.overrideredirect(1)
        loading.wm_attributes()
        loading.wm_attributes('-disabled', True)
        # loading.wm_attributes("-alpha", 0.9)
        loading.wm_geometry('200x70')
        root.eval(f'tk::PlaceWindow {str(loading)} center')

        loading_lab = wdg.EntryName(loading, text='\nProceso en ejecución...\n\nPor favor espere.\n')
        loading_lab.pack(fill='both')
        loading.focus_force()
        while t.is_alive():
            root.update()
        # out = summation.exec(logic.getPlaces(os.getenv('root')))
    except AttributeError as e:
        ms.showerror(title="Format Error", message=e)
    except:
        ms.showerror(title='Unknown Error', message="Has occured an error")
    else:
        loading.destroy()
        text = f"Archivo {out['filename']} creado en {out['filedir']} con {out['nrecs']} registros."
        ms.showinfo(title="Tarea Finalizada", message=text)


def _getSep(inpSep=None, sep=None):
    # inpSep = [coma, tab, other]
    outSep = [',', '\t', sep]
    for b in zip(inpSep, outSep):
        if b[0]:
            return b[1]


def masiveAddCommand(pathfile, targetpath, inpSep, sep, encod, headers, numfields):
    if pathfile != '' and targetpath != '':
        try:
            numeration = list(map(int, numfields))
        except:
            numeration = None
        
        try:
            records = logic.attsFromFile(pathfile, _getSep(inpSep,sep), headers, numeration, encod)
        except:
            ms.showerror(message="Wrong value")
        else:
            records = logic.attsFromFile(pathfile, _getSep(inpSep,sep), headers, numeration, encod)
            n, y = 0, 0
            for record in records:
                city = record['name'].lower().replace(' ', '-')
                folder = targetpath.replace('/', os.sep) + os.sep + record['name']
                if logic.newPlace(root=os.getenv('root'), url=record['url'], targetpath=folder, cityname=city)[0]:
                    y += 1
                else:
                    n += 1
            ms.showinfo(message='Tarea Completada:\n\n{} registro(s) nuevo(s)\n{} registro(s) omitido(s) por duplicidad'.format(y,n))
    
    else:
        ms.showwarning(title="Field Empty", message="Input or Output field is not complete")


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
                                  targetpath=folder.replace('/', os.sep), cityname=city)
            if cityname is None:
                ms.showerror(title="Not URL", message="URL value does not have a correct structure")
            elif cityname[0]:
                ms.showinfo(title="New city added",
                            message=f"'{name}' HAS ADDED AS '{cityname[1]}'")
            else:
                ms.showinfo(title="City Duplicity",
                            message=f"'{cityname[1]}' already exists")
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
    print(masiveAddCommand(os.getenv('filetest'), os.getenv('absdir'), [0,1,0], None, '', False, [1,2]))
