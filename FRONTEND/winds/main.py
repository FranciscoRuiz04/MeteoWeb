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

#-----------------------    GPS Pckgs    ----------------------#
## Module importation to exec file creation
from FRONTEND import commands
from FRONTEND import widgets as wdg

## Module importation to be developing
# try:
#     import widgets as wdg
# except ModuleNotFoundError:
#     import sys
#     sys.path.append(r'C:\CODES\MeteoWeb\FRONTEND')
#     import widgets as wdg
    # import commands
#--------------------------------------------------------------#
def win(root):
    # Root window
    root = tk.Toplevel(root)
    root.geometry('616x220')
    root.resizable(False, False)
    root.config(bg='#818284')
    root.title('Registros')
    root.focus_force()
    
    div7 = wdg.LabelFrame(root, bg='#858784', height=8)
    div7.pack(padx=6, fill='x')


    #####################       Content Brief    ##########################
    #####################          Header        ##########################

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
    # header3.grid(row=0, column=0)
    header3.pack(side='left', fill='both')

    header31 = tk.Label(div5,
                        text='Carpeta',
                        font=('Arial', 10, 'bold'),
                        bg='#134351',
                        fg='#FFBB05',
                        justify='center',
                        relief='raised')
    # header31.grid(row=0, column=1)
    header31.pack(side='left', fill='both', expand=True)

    # +++++++++++++++++++++++++       Dataframe    +++++++++++++++++++++++++#

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
                        width=45)
        webent2.grid(row=n, column=1, sticky='ew')


    # root.mainloop()
