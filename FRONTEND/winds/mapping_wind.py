__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "2.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


######################       Packages    ##########################

import tkinter as tk
import os
#-----------------------    GPS Pckgs    ----------------------#

# Developing
from FRONTEND import commands, widgets as wdg
#--------------------------------------------------------------#


def importwind(rootmain):
    # Root window
    root = tk.Toplevel(rootmain)
    root.geometry('460x230')
    root.resizable(False, False)
    root.config(bg='#818284')
    # Window title
    root.title('Generador de Mapas')
    
    root.focus_force()
    div1 = wdg.LabelFrame(root)
    div1.pack(fill='x', padx=10, pady=10)

    h1 = wdg.SectionName(div1, 'Archivo de Salida')
    h1.grid(row=0, column=0, padx=10, pady=3)

    l1 = wdg.EntryName(div1, 'Nombre')
    l1.grid(row=1, column=0, pady=7)
    
    fileName = tk.StringVar()
    i1 = wdg.Entry(div1, 30, fileName)
    i1.grid(row=1, column=1, sticky='w', columnspan=2)
    
    l2 = wdg.EntryName(div1, 'Ruta')
    l2.grid(row=2, column=0, pady=7)

    pathfile2 = tk.StringVar()
    i1 = wdg.Entry(div1, 30, pathfile2)
    i1.grid(row=2, column=1, sticky='w', columnspan=2)
    
    b1 = wdg.SearchBtm(div1, 'Buscar', pathfile2)
    b1.grid(row=2, column=3, padx=10)
    
    # Parameters Section
    h2 = wdg.SectionName(div1, 'Parámetros')
    h2.grid(row=3, column=0, padx=10, pady=3)
    
    l3 = wdg.EntryName(div1, 'Día')
    l3.grid(row=4, column=0, pady=7)
    # Day Selection List
    selected_day=tk.StringVar()
    itemsList1 = tk.ttk.Combobox(div1, textvariable=selected_day, width=1)
    itemsList1['values'] = [v for v in range(1,8)]
    itemsList1['state'] = 'readonly'
    itemsList1.grid(row=4, column=1, sticky='w')
    
    l4 = wdg.EntryName(div1, 'Variable')
    l4.grid(row=4, column=2, pady=7, sticky='w')
    # Meteorological Varaible Selection List
    selected_var=tk.StringVar()
    itemsList1 = tk.ttk.Combobox(div1, textvariable=selected_var, width=6)
    itemsList1['values'] = ['pp', 'p', 'tmin', 'tmax', 'ws']
    itemsList1['state'] = 'readonly'
    itemsList1.grid(row=4, column=3, sticky='w')
    
    sendBtm = wdg.Button(root, 'Listo', lambda: commands.mapping(pathfile2.get(), fileName.get(), selected_day.get(), selected_var.get()))
    sendBtm.pack()