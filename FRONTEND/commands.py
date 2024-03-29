
__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "2.0.3"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

########################    Packages    ########################

import os, sys
from tkinter import messagebox as ms
from threading import Thread
from dotenv import load_dotenv as env
import tkinter as tk
env()

## Module importation to exec file creation
sys.path.append(os.getenv('mainFolder'))

import widgets as wdg
from BACKEND import logic
from BACKEND import summation
from BACKEND import main
from BACKEND.meteoweb import mappers
from BACKEND.meteoweb import creators


#--------------------------------------------------------------#



def forecast(root):
    try:
        t = Thread(target=main.exec, daemon=True)
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
        text = f"Pronóstico Generado"
        ms.showinfo(title="Tarea Finalizada", message=text)

def foreteenFC(root):
    try:
        t = Thread(target=main.exec14, daemon=True)
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
        text = f"Pronóstico Generado"
        ms.showinfo(title="Tarea Finalizada", message=text)

def __myfun(targetpath, daily=True):
    global out
    if daily:
        out = summation.exec(logic.getPlaces(os.getenv('root')), targetpath)
    else:
        out = summation.exec14(logic.getPlaces(os.getenv('root')), targetpath)

def summarize(root, targetpath, daily):
    try:
        t = Thread(target=lambda: __myfun(targetpath, daily), daemon=True)
        t.start()
        loading = tk.Toplevel(root)
        loading.title('Running Process')
        # loading.overrideredirect(1)
        loading.wm_attributes()
        loading.wm_attributes('-disabled', True)
        # loading.wm_attributes("-alpha", 0.9)
        loading.wm_geometry('200x70')
        # root.eval(f'tk::PlaceWindow {str(loading)} center')

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


def mapping(mainDir, z_value, methodList=('UK','IDW')):
    assert mainDir != '', ms.showerror(title='Empty Parameter', message='Enter a valid value')
    
    # File paths generation
    fileTypes = ['png', 'txt']
    genFilePaths = (path[1] + os.sep + method for method in methodList for path in creators.pathsIter2Map([1, 4], mainDir))
    genFiles = [basepath + '.' + fileType for basepath in genFilePaths for fileType in fileTypes]

    parmsList = []
    n = 0
    while True:
        pair = tuple(genFiles[n : n+2])
        # Assing an intepolation method
        if n < 6: m = 'UK'  # 6 first items correspon to 'UK' method. Including item number 0.
        else:
            m = 'IDW'
            pair = pair[0]
        
        eachParm = {'path':pair, 'method':m}
        parmsList.append(eachParm)
        
        n += 2
        if n == 12 or len(methodList) == 1 and n % 6 == 0: break
    s = 0
    parmsDic = {}
    while True:
        byFolderList = parmsList[s], parmsList[s+3]
        parmsDic[s+1] = byFolderList
        s += 1
        if s == 3: break
    # return parmsDic
    try:
        s,n = 0, 0
        for day in range(1, 4):
            myclass = mappers.Mappers(day, z_value)
            for method in parmsDic[day]:
                methodName = method['method']
                if methodName == 'IDW':
                    cacher = myclass.chooseMethod(method=methodName, save_path=method['path'])
                else:
                    cacher = myclass.chooseMethod(method=methodName, save_list=method['path'])
    
                if cacher=='VUD': s += 1
                elif cacher=='IUD': n += 1
    except AttributeError as e:
        ms.showerror(title="Format Error", message=e)
    except:
        ms.showerror(title='Unknown Error', message="Has occured an error")
    else:
        text = f"Archivos creados en {mainDir}\nVUD: {s}\tIUD: {n}"
        ms.showinfo(title="Tarea Finalizada", message=text)

def _getSep(inpSep=None, sep=None):
    # inpSep = [coma, tab, other]
    outSep = [',', '\t', sep]
    for b in zip(inpSep, outSep):
        if b[0]:
            return b[1]

def _getMethod(inpMethod=None):
    # inpSep = [coma, tab, other]
    outMet = ['UK', 'IDW']
    for b in zip(inpMethod, outMet):
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


def dropMassive(inp):
    n = 0
    for key, value in inp.items():
        if value.get():
            if logic.dropPlace(root=os.getenv('root'), cityname=key):
                n += 1
    ms.showinfo(title="Dropped", message=f"{n} records have been dropped")


def dropWhole():
    warn = ms.askokcancel(title='Warning', message='You are about to delete all the records from DB.\nAre you sure?')
    if warn:
        try:
            logic.cleanDB(os.getenv('root'))
        except FileExistsError:
            ms.showerror(title='Fatal Error', message='Something was wrong. Records have not been deleted')
        else:
            ms.showinfo(title='Clean whole', message='All locations deleted')


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
    mapping(r'C:/Users/Francisco Ruiz/Desktop/mw', 'tmax')
    # import pprint
    # pprint.pprint(mapping(r'C:/Users/Francisco Ruiz/Desktop/mw', 'tmin'))
    # print(mapping(r'C:/Users/Francisco Ruiz/Desktop/mw', 'tmin'))
#     print(masiveAddCommand(os.getenv('filetest'), os.getenv('absdir'), [0,1,0], None, '', False, [1,2]))
