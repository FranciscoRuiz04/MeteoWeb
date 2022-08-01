__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

########################    Packages    ########################
import tkinter as tk
from tkinter import LEFT, RIGHT, ttk
import os

#-----------------------    GPS Pckgs    ----------------------#
# from FRONTEND import commands
import commands
try:
    import widgets as wdg
except ModuleNotFoundError:
    import sys
    sys.path.append(r'C:\CODES\MeteoWeb\FRONTEND')
    import widgets as wdg
#--------------------------------------------------------------#

# Root window
root = tk.Tk()
root.geometry('760x600')
root.resizable(False, False)
root.config(bg='#818284')
root.title('MeteoWeb')
logo = tk.PhotoImage(file=os.getenv('logopath'))
root.iconphoto(True, logo)


######################       New Location    ##########################
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


######################       Separator    ##########################
div2 = wdg.LabelFrame(root, 3)
div2.pack(padx=6, fill='x')


######################       Drop Location    ##########################
div3 = wdg.LabelFrame(root)
div3.pack(fill='x', padx=10, pady=10)

header2 = wdg.SectionName(div3, 'Borrar Locación')
header2.grid(row=0, column=0, padx=10, pady=3)

# Cityname
namLab = wdg.EntryName(div3, 'Nombre')
namLab.grid(row=1, column=0, pady=7)

ent4 = wdg.Entry(div3)
ent4.grid(row=1, column=1)

btn2 = wdg.Button(div3, 'Borrar', lambda: commands.dropCommand(ent4.get()))
btn2.grid(row=4, column=1, pady=10)


######################       Separator    ##########################

div4 = wdg.LabelFrame(root, 3)
div4.pack(padx=6, fill='x')

div7 = wdg.LabelFrame(root, bg='#858784', height=10)
div7.pack(padx=6, fill='x')


######################       Content Brief    ##########################
######################          Header        ##########################

div5 = wdg.LabelFrame(root)
div5.pack(fill='x', padx=10)

header3 = tk.Label(div5,
                   text='Nombre',
                   font=('Arial', 10, 'bold'),
                   bg='#134351',
                   fg='#FFBB05',
                   relief='raised',
                   height=2,
                   width=25)
header3.grid(row=0, column=0)
header3.pack(side='left', fill='both')

header31 = tk.Label(div5,
                    text='Carpeta',
                    font=('Arial', 10, 'bold'),
                    bg='#134351',
                    fg='#FFBB05',
                    justify='center',
                    relief='raised',
                    height=2,
                    width=45)
# header31.grid(row=0, column=1)
header31.pack(side='left', fill='both', expand=True)

#+++++++++++++++++++++++++       Dataframe    +++++++++++++++++++++++++#

div6 = tk.LabelFrame(root,
                     bg='#858784',
                     relief='flat')
div6.pack(fill='both', padx=10, expand=True)

mycanvas = tk.Canvas(div6, bg='#134351', relief='flat')
mycanvas.pack(side=LEFT, fill='both', expand=True)

style = ttk.Style()
style.theme_use("default")
style.configure("Vertical.TScrollbar",
                background="#002366", arrowcolor="#F1C40F")


yscroll = ttk.Scrollbar(div6, orient='vertical', command=mycanvas.yview)
yscroll.pack(side=RIGHT, fill='y')

mycanvas.configure(yscrollcommand=yscroll.set)
mycanvas.bind('<Configure>', lambda e: mycanvas.configure(
    scrollregion=mycanvas.bbox('all')))

myframe = tk.Frame(mycanvas, bg='#134351', relief='flat')
mycanvas.create_window((0, 0), window=myframe, anchor='nw')

for n, val in enumerate(commands.brief(), 2):
    data1 = tk.StringVar()
    data1.set(val[0])
    webent = tk.Entry(myframe,
                      textvariable=data1,
                      font=('Arial', 11, 'bold'),
                      bg='#134351',
                      foreground='white',
                      width=25)
    webent.grid(row=n, column=0, sticky='ew', pady=5)

    data2 = tk.StringVar()
    data2.set(val[1])
    webent2 = tk.Entry(myframe,
                       textvariable=data2,
                       font=('Arial', 11, 'bold'),
                       bg='#134351',
                       foreground='white',
                       width=62)
    webent2.grid(row=n, column=1, sticky='ew')


######################       Separator    ##########################
# div8 = tk.wdg.LabelFrame(root, bg='#002366', height=20, relief='flat')
# div8.pack(padx=6, fill='x')


root.mainloop()
