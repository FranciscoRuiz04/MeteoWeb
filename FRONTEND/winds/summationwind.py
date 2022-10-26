__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "2.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


######################       Packages    ##########################

import tkinter as tk
#-----------------------    GPS Pckgs    ----------------------#

# Developing
from FRONTEND import commands, widgets as wdg
#--------------------------------------------------------------#


def importwind(rootmain, daily):
    # Root window
    root = tk.Toplevel(rootmain)
    root.geometry('450x125')
    root.resizable(False, False)
    root.config(bg='#818284')
    root.title('Resumen')
    root.focus_force()
    div1 = wdg.LabelFrame(root)
    div1.pack(fill='x', padx=10, pady=10)

    h1 = wdg.SectionName(div1, 'Ruta de Salida')
    h1.grid(row=0, column=0, padx=10, pady=3)

    l1 = wdg.EntryName(div1, 'Ruta')
    l1.grid(row=1, column=0, pady=7)

    pathfile = tk.StringVar()
    i1 = wdg.Entry(div1, 30, pathfile)
    i1.grid(row=1, column=1, sticky='w')
    
    b1 = wdg.SearchBtm(div1, 'Buscar', pathfile)
    b1.grid(row=1, column=2, padx=10)
    
    sendBtm = wdg.Button(root, 'Listo',
                         lambda: commands.summarize(root, pathfile.get(), daily))
    sendBtm.pack()