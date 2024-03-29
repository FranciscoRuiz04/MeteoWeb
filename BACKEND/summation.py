__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "2.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


########################    Packages    ########################
import pandas as pd
import os
#-----------------------    GPS Pckgs    ----------------------#
## Module importation running from MeteoWeb.py (C:\CODES\MeteoWeb)
from BACKEND.meteoweb import creators

#--------------------------------------------------------------#

def exec(gen, targetpath):
    df = pd.DataFrame(columns=["Loc", "%", "mm", "°C_min",
                                   "°C_max", "km/h", "WindDir",
                                   "Date"])
    numrecs = 0
    for g in gen:
        objClass = creators.File_Brief(g, 'txt')
        for rec in objClass.FormatRecords():
            df.loc[len(df)] = rec
            numrecs += 1
    objClass.Filename()
    targetpath += os.sep + 'Concentrado_' + objClass.filename
    df.to_csv(targetpath, encoding='utf-8',index_label='ID')
    return {"nrecs":numrecs, "filedir":os.path.dirname(targetpath), "filename":os.path.basename(targetpath)}


def exec14(gen, targetpath):
    df = pd.DataFrame()
    numrecs = 0
    for g in gen:
        objClass = creators.File_Brief14(g, 'txt')
        unit_df = objClass.FormatRecords()
        df = pd.concat([df, unit_df])
        numrecs += 14
    
    df.reset_index(inplace=True, drop=True)
    objClass.Filename()
    fname = 'Concentrado14' + "_" + objClass.filename
    targetpath += os.sep + fname
    
    df.reset_index(inplace=True, drop=True) # Patch bug at index order since index repeat for every city
    df.to_csv(targetpath, encoding='utf-8',index_label='ID')
    return {"nrecs":numrecs, "filedir":os.path.dirname(targetpath), "filename":os.path.basename(targetpath)}

#--------------------------------------------------------------#
# import logic
# exec14(logic.getPlaces(os.getenv('root')), '.')

#--------------------------------------------------------------#
