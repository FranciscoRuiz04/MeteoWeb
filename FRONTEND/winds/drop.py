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


def drop(root):
    # Root window
    root = tk.Toplevel(root)
    root.geometry('616x100')
    root.resizable(False, False)
    root.config(bg='#818284')
    root.title('Borrar Registro')

    # Main Frame
    div3 = wdg.LabelFrame(root)
    div3.pack(fill='x', padx=10, pady=10)

    header2 = wdg.SectionName(div3, 'Borrar Locación')
    header2.grid(row=0, column=0, padx=10, pady=3)

    # Cityname
    namLab = wdg.EntryName(div3, 'Nombre')
    namLab.grid(row=1, column=0, pady=7)

    ent4 = wdg.Entry(div3, 45)
    ent4.grid(row=1, column=1)

    btn2 = wdg.Button(
        div3, 'Borrar', lambda: commands.dropCommand(ent4.get()), 10)
    btn2.grid(row=1, column=2, pady=10, padx=20)

    # root.mainloop()
