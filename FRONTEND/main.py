__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"

########################    Packages    ########################
from doctest import master
import tkinter as tk
from tkinter import LEFT, RIGHT, ttk
import os
#-----------------------    GPS Pckgs    ----------------------#
# from FRONTEND import commands
import commands
#--------------------------------------------------------------#

# Root window
root = tk.Tk()
root.geometry('750x600')
root.resizable(False, False)
root.config(bg='#818284')
root.title('MeteoWeb')
logo = tk.PhotoImage(file=os.getenv('logopath'))
root.iconphoto(True, logo)

######################       New Location    ##########################


class LabelFrame(tk.LabelFrame):
    def __init__(self, height=0, bg='#134351'):
        tk.LabelFrame.__init__(
            self, master=root, bg=bg, relief='flat', height=height)


class SectionName(tk.Label):
    def __init__(self, div, text):
        tk.Label.__init__(self, master=div, text=text, font=(
            'Arial', 9, 'bold'), bg='#134351', fg='#FFBD08')


class EntryName(tk.Label):
    def __init__(self, div, text, relief=None, height=None, width=None):
        tk.Label.__init__(self, master=div, text=text, font=(
            'Arial', 10, 'bold'), bg='#134351', fg='#dcdcdc', padx=10, relief=relief, height=height, width=width)


class Entry(tk.Entry):
    def __init__(self, div):
        tk.Entry.__init__(self, master=div, width=75, font=(
            'Arial', 10), borderwidth=3, exportselection=True, justify='center', bg='#dcdcdc', fg='black')


class Button(tk.Button):
    def __init__(self, div, text, functionality):
        tk.Button.__init__(self, master=div, text=text, font=('Arial', 11, 'bold'), border=3,
                           relief='ridge', bg='#134351', fg='#FFBD07', width=8, command=functionality)





div1 = LabelFrame()
div1.pack(fill='x', padx=10, pady=10)

header1 = SectionName(div1, 'Nueva Locación')
header1.grid(row=0, column=0, padx=10, pady=3)

# URL
urlLab = EntryName(div1, 'URL')
urlLab.grid(row=1, column=0, pady=7)

ent = Entry(div1)
ent.grid(row=1, column=1, sticky='w')

# Target Path
targetLab = EntryName(div1, 'Carpeta')
targetLab.grid(row=2, column=0, pady=7)

ent2 = Entry(div1)
ent2.grid(row=2, column=1, sticky='w')

# Cityname
cityLab = EntryName(div1, 'Nombre')
cityLab.grid(row=3, column=0, pady=7)

ent3 = Entry(div1)
ent3.grid(row=3, column=1)

# Add bottom
btn1 = Button(div1, 'Añadir', lambda: commands.addCommand(
    ent.get(), ent2.get(), ent3.get()))
btn1.grid(row=4, column=1, pady=10)


######################       Separator    ##########################
div2 = LabelFrame(3)
div2.pack(padx=6, fill='x')


######################       Drop Location    ##########################
div3 = LabelFrame()
div3.pack(fill='x', padx=10, pady=10)

header2 = SectionName(div3, 'Borrar Locación')
header2.grid(row=0, column=0, padx=10, pady=3)

# Cityname
namLab = EntryName(div3, 'Nombre')
namLab.grid(row=1, column=0, pady=7)

ent4 = Entry(div3)
ent4.grid(row=1, column=1)

btn2 = Button(div3, 'Borrar', lambda: commands.dropCommand(ent4.get()))
btn2.grid(row=4, column=1, pady=10)


######################       Separator    ##########################

div4 = LabelFrame(3)
div4.pack(padx=6, fill='x')

div7 = LabelFrame(bg='#858784', height=10)
div7.pack(padx=6, fill='x')


######################       Content Brief    ##########################
######################          Header        ##########################

div5 = LabelFrame()
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
# div8 = tk.LabelFrame(root, bg='#002366', height=20, relief='flat')
# div8.pack(padx=6, fill='x')


root.mainloop()
