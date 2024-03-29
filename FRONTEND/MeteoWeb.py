__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "3.0.0"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


######################       Packages    ##########################

import tkinter as tk
import os
from dotenv import load_dotenv as env
env()
#-----------------------    GPS Pckgs    ----------------------#
## Module importation to exec file creation
from winds import main
from winds import dropping
from winds import fromfile
from winds import newrecord
from winds import summationwind
from winds import mapping_wind
import widgets as wdg
import commands as commands
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

reporTool = wdg.MenuBar(statOpts)
statOpts.add_cascade(label='Resumen', menu=reporTool)
reporTool.add_command(label='7 días', command=lambda:summationwind.importwind(root, daily=True))
reporTool.add_command(label='14 días', command=lambda:summationwind.importwind(root, daily=False))


forecast = wdg.MenuBar(statOpts)
statOpts.add_cascade(label='Pronóstico', menu=forecast)
forecast.add_command(label='7 días', command=lambda: commands.forecast(root))
forecast.add_command(label='14 días', command=lambda: commands.foreteenFC(root))

statOpts.add_command(label='Mapa', command= lambda: mapping_wind.importwind(root))

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
