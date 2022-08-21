__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


########################    Packages    ########################
import pandas as pd
import os
#-----------------------    GPS Pckgs    ----------------------#

from meteoweb import creators
import logic
#--------------------------------------------------------------#

def exec(gen):
    df = pd.DataFrame(columns=["Loc", "%", "mm", "°C_min",
                                   "°C_max", "km/h", "WindDir",
                                   "Date"])
    for g in gen:
        objClass = creators.File_Brief(g, 'txt', 'utf-8')
        for rec in objClass.FormatRecords():
            df.loc[len(df)] = rec
    objClass.FilePath()
    df.to_csv(objClass.filepath, encoding='utf-8',index_label='ID')

#--------------------------------------------------------------#

exec(logic.getPlaces(os.getenv('root')))

#--------------------------------------------------------------#
