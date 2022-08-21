__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


######################       Packages    ##########################

import tkinter as tk
#-----------------------    GPS Pckgs    ----------------------#

from FRONTEND import widgets as wdg
from FRONTEND import commands
#--------------------------------------------------------------#


def new(root):
    # Root window
    root = tk.Toplevel(root)
    root.geometry('760x210')
    root.resizable(False, False)
    root.config(bg='#818284')
    root.title('Nueva Locación')
    root.focus_force()

    ######################     Frame      ##########################
    div1 = wdg.LabelFrame(root)
    div1.pack(fill='x', padx=10, pady=10)

    header1 = wdg.SectionName(div1, 'Nueva Locación')
    header1.grid(row=0, column=0, padx=10, pady=3)

    # URL
    urlLab = wdg.EntryName(div1, 'URL')
    urlLab.grid(row=1, column=0, pady=7)

    ent = wdg.Entry(div1)
    ent.grid(row=1, column=1, sticky='w')

    # Target Path
    targetLab = wdg.EntryName(div1, 'Carpeta')
    targetLab.grid(row=2, column=0, pady=7)

    p = tk.StringVar()
    ent2 = wdg.Entry(div1, text=p)
    ent2.grid(row=2, column=1, sticky='w')

    bsearch = wdg.SearchBtm(div1, 'Buscar', p)
    bsearch.grid(row=2, column=2, padx=10)
    # Cityname
    cityLab = wdg.EntryName(div1, 'Nombre')
    cityLab.grid(row=3, column=0, pady=7)

    ent3 = wdg.Entry(div1)
    ent3.grid(row=3, column=1)

    # Add bottom
    btn1 = wdg.Button(div1, 'Añadir', lambda: commands.addCommand(
        ent.get(), ent2.get(), ent3.get()))
    btn1.grid(row=4, column=1, pady=10)

    # root.mainloop()
