__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


######################       Packages    ##########################
from tkinter import LEFT, RIGHT, ttk
import tkinter as tk
import sys, os
# from dotenv import load_dotenv as env

#-----------------------    GPS Pckgs    ----------------------#
# env()

## Module importation to exec file creation
# from FRONTEND import widgets as wdg
# from FRONTEND import commands

## Module importation to be developing and distribution
sys.path.append(os.getenv('BACKENDMods'))
sys.path.append(os.getenv('FRONTENDMods'))
import widgets as wdg
import commands

def dropping(root):
    root = tk.Toplevel(root)
    root.geometry('500x500')
    root.resizable(False, False)
    root.config(bg='#818284')
    root.title('Borrar Registro')
    root.focus_force()
    

    # Dataframe Header
    div2 = wdg.LabelFrame(root)
    div2.pack(fill='x', padx=10)

    header = tk.Label(div2,
                    text='Borrar',
                    font=('Arial', 10, 'bold'),
                    bg='#134351',
                    fg='#FFBB05',
                    relief='raised',
                    height=2,
                    width=12)
    header.pack(side='left', fill='both')

    header2 = tk.Label(div2,
                    text='Identificador',
                    font=('Arial', 10, 'bold'),
                    bg='#134351',
                    fg='#FFBB05',
                    relief='raised',
                    height=2,
                    width=50)
    header2.pack(side='left', fill='both')


    # Dataframe creation with right scrollbar
    div = tk.LabelFrame(root,
                            bg='#858784',
                            relief='flat')
    div.pack(fill='both', padx=10, expand=True)

    mycanvas = tk.Canvas(div, bg='#134351', relief='flat')
    mycanvas.pack(side=LEFT, fill='both', expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Vertical.TScrollbar",
                    background="#002366", arrowcolor="#F1C40F")


    yscroll = ttk.Scrollbar(div, orient='vertical', command=mycanvas.yview)
    yscroll.pack(side=RIGHT, fill='y')

    mycanvas.configure(yscrollcommand=yscroll.set)
    mycanvas.bind('<Configure>', lambda e: mycanvas.configure(
        scrollregion=mycanvas.bbox('all')))

    myframe = tk.Frame(mycanvas, bg='#134351', relief='flat')
    mycanvas.create_window((0, 0), window=myframe, anchor='nw')

    data = {}
    # Data displaying
    for n, val in enumerate(commands.brief(), 2):
        # Cityname label
        data1 = tk.StringVar()
        data1.set(val[0])
        webent = tk.Entry(myframe,
                        textvariable=data1,
                        font=('Arial', 11, 'bold'),
                        bg='#134351',
                        foreground='white',
                        width=40)
        webent.grid(row=n, column=1, pady=5, padx=10)


        # Checkbox
        cb_value = tk.IntVar()
        cb = wdg.CB(myframe, '', lambda: wdg.checkBx(cb_value), cb_value)
        cb.grid(row=n, column=0, padx=35)
        data[val[0]] = cb_value



    sendBtm = wdg.Button(root, 'Listo', lambda: commands.dropMassive(data))
    sendBtm.pack()

    # root.mainloop()