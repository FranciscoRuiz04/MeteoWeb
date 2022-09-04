__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.3"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


######################       Packages    ##########################

import tkinter as tk
import os, sys
from dotenv import load_dotenv as env
env()
sys.path.append(os.getenv('BACKENDMods'))
sys.path.append(os.getenv('FRONTENDMods'))
#-----------------------    GPS Pckgs    ----------------------#
## Module importation to exec file creation
# from FRONTEND.winds import main, drop, fromfile, newrecord
# from FRONTEND import widgets as wdg
# from FRONTEND import commands

# Module importation to be developing and distribution
from winds import main, drop, fromfile, newrecord
import widgets as wdg
import commands
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
toolsmenu.add_command(label='Borrar', command=lambda: drop.drop(root))
options.add_command(label="Desde Archivo",
                    command=lambda: fromfile.importwind(root))
options.add_command(label='Manual', command=lambda: newrecord.new(root))
toolsmenu.add_cascade(label='Nuevo', menu=options)
toolsmenu.add_separator()

statOpts = wdg.MenuBar(toolsmenu)
statOpts.add_command(label='Pronóstico', command=lambda: commands.forecast(root))
statOpts.add_command(label='Resumen', command=lambda:commands.summarize(root))
toolsmenu.add_cascade(label='Generar', menu=statOpts)

helpmenu = wdg.MenuBar(menubar)
helpmenu.add_command(label="Acerca de")
menubar.add_cascade(label="Ayuda", menu=helpmenu)

root.config(menu=menubar)


######################       Background logo    ##########################
logoimg = tk.PhotoImage(file=os.getenv('mainlogopath'))
img = logoimg.subsample(10, 10)
panel = tk.Label(root, image=img, bg='#272727')
panel.pack(fill='both')


root.mainloop()
