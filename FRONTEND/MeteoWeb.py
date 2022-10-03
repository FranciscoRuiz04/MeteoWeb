__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "2.0.0"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


######################       Packages    ##########################

import tkinter as tk
import os, sys
from dotenv import load_dotenv as env
env()

#-----------------------    GPS Pckgs    ----------------------#
## Module importation to exec file creation
from FRONTEND.winds import main, dropping, fromfile, newrecord, summationwind
from FRONTEND import widgets as wdg
from FRONTEND import commands

# Module importation to be developing and distribution
# sys.path.append(os.getenv('BACKENDMods'))
# sys.path.append(os.getenv('FRONTENDMods'))
# from winds import main, dropping, fromfile, newrecord, summationwind
# import widgets as wdg
# import commands
#--------------------------------------------------------------#


######################       Root window    ##########################
root = tk.Tk()
root.geometry('220x145')
root.resizable(False, False)
root.config(bg='#818284')
root.title('Inicio')
logo = tk.PhotoImage(file=os.getenv('logopath'))
root.iconphoto(True, logo)

# root.eval('tk::PlaceWindow . center')


######################       Menu Bar    ##########################
menubar = wdg.MenuBar(root)

home = wdg.MenuBar(menubar)
home.add_command(label='Registros', command=lambda: main.win(root))
menubar.add_cascade(label='Ver', menu=home)

toolsmenu = wdg.MenuBar(menubar)
menubar.add_cascade(label="Herramientas", menu=toolsmenu)

options = wdg.MenuBar(toolsmenu)
options.add_command(label="Desde Archivo",
                    command=lambda: fromfile.importwind(root))
options.add_command(label='Manual', command=lambda: newrecord.new(root))
toolsmenu.add_cascade(label='Nuevo', menu=options)

dropOpts = wdg.MenuBar(toolsmenu)
toolsmenu.add_cascade(label='Borrar', menu=dropOpts)
dropOpts.add_command(label='Por Selección', command=lambda: dropping.dropping(root))
dropOpts.add_command(label='Todo', command=commands.dropWhole)

toolsmenu.add_separator()


statOpts = wdg.MenuBar(toolsmenu)
toolsmenu.add_cascade(label='Generar', menu=statOpts)
statOpts.add_command(label='Resumen', command=lambda:summationwind.importwind(root))

forecast = wdg.MenuBar(statOpts)
statOpts.add_cascade(label='Pronóstico', menu=forecast)
forecast.add_command(label='Diario', command=lambda: commands.forecast(root))
forecast.add_command(label='14 días', command=lambda: commands.foreteenFC(root))

# helpmenu = wdg.MenuBar(menubar)
# helpmenu.add_command(label="Acerca de")
# menubar.add_cascade(label="Ayuda", menu=helpmenu)

root.config(menu=menubar)


######################       Background logo    ##########################
logoimg = tk.PhotoImage(file=os.getenv('mainlogopath'))
img = logoimg.subsample(10, 10)
panel = tk.Label(root, image=img, bg='#272727')
panel.pack(fill='both')


root.mainloop()
