import tkinter as tk
from tkinter import LEFT, RIGHT, ttk
from FRONTEND import commands
import os

# Root window
root = tk.Tk()
root.geometry('850x600')
root.resizable(False, False)
root.config(bg='#002366')
root.title('MeteoWeb')
logo = tk.PhotoImage(file=os.getenv('logopath'))
root.iconphoto(True, logo)

######################       New Location    ##########################
div1 = tk.LabelFrame(root,
                     bg='#003153',
                     relief='flat')
div1.pack(fill='x', padx=10, pady=10)

header1 = tk.Label(div1,
                   text='Nueva Locación',
                   font=('Arial', 10, 'bold'),
                   bg='#003153',
                   fg='#F1C40F')
header1.grid(row=0, column=0, padx=10, pady=3)

# URL
urlLab = tk.Label(div1,
                  text='URL',
                  font=('Arial', 11, 'bold'),
                  bg='#003153',
                  foreground='#dcdcdc',
                  padx=10)
urlLab.grid(row=1, column=0, pady=7)

ent = tk.Entry(div1, width=75, font=('Arial', 12),
               borderwidth=3,
               exportselection=True,
               justify='center',
               bg='#dcdcdc', fg='black')
ent.grid(row=1, column=1)

# Target Path
targetLab = tk.Label(div1,
                     text='Carpeta',
                     font=('Arial', 11, 'bold'),
                     bg='#003153',
                     foreground='#dcdcdc',
                     padx=10)
targetLab.grid(row=2, column=0, pady=7)

ent2 = tk.Entry(div1, width=75, font=('Arial', 12),
                borderwidth=3,
                exportselection=True,
                justify='center',
                bg='#dcdcdc', fg='black')
ent2.grid(row=2, column=1)

# Cityname
cityLab = tk.Label(div1,
                   text='Nombre',
                   font=('Arial', 11, 'bold'),
                   bg='#003153',
                   foreground='#dcdcdc',
                   padx=10)
cityLab.grid(row=3, column=0, pady=7)

ent3 = tk.Entry(div1, width=75, font=('Arial', 12),
                borderwidth=3,
                exportselection=True,
                justify='center',
                bg='#dcdcdc', fg='black')
ent3.grid(row=3, column=1)

# Add bottom
btn1 = tk.Button(div1,
                 text='Añadir',
                 font=('Arial', 12, 'bold'),
                 border=3,
                 relief='ridge',
                 bg='#002366',
                 fg='#F1C40F',
                 width=8,
                 command=lambda: commands.addCommand(ent.get(), ent2.get(), ent3.get()))
btn1.grid(row=4, column=1, pady=10)


######################       Separator    ##########################

div2 = tk.LabelFrame(root, bg='#F1C40F', height=3, relief='flat')
div2.pack(padx=6, fill='x')


######################       Drop Location    ##########################
div3 = tk.LabelFrame(root,
                     bg='#003153',
                     relief='flat')
div3.pack(fill='x', padx=10, pady=10)

header2 = tk.Label(div3,
                   text='Borrar Locación',
                   font=('Arial', 10, 'bold'),
                   bg='#003153',
                   fg='#F1C40F')
header2.grid(row=0, column=0, padx=10, pady=3)

# Cityname
namLab = tk.Label(div3,
                  text='Nombre',
                  font=('Arial', 11, 'bold'),
                  bg='#003153',
                  foreground='#dcdcdc',
                  padx=10)
namLab.grid(row=1, column=0, pady=7)

ent4 = tk.Entry(div3,
                width=75,
                font=('Arial', 12),
                borderwidth=3,
                exportselection=True,
                justify='center',
                bg='#dcdcdc', fg='black',)
ent4.grid(row=1, column=1)

btn2 = tk.Button(div3,
                 text='Borrar',
                 font=('Arial', 12, 'bold'),
                 border=3,
                 relief='ridge',
                 bg='#002366',
                 fg='#F1C40F',
                 width=8,
                 command=lambda: commands.dropCommand(ent4.get()))
btn2.grid(row=4, column=1, pady=10)


######################       Separator    ##########################

div4 = tk.LabelFrame(root, bg='#F1C40F', height=3, relief='flat')
div4.pack(padx=6, fill='x')

div7 = tk.LabelFrame(root, bg='#002366', height=10, relief='flat')
div7.pack(padx=6, fill='x')


######################       Content Brief    ##########################
######################          Header        ##########################

div5 = tk.LabelFrame(root,
                     bg='#003153',
                     relief='flat')
div5.pack(fill='x', padx=10)

header3 = tk.Label(div5,
                   text='Nombre',
                   font=('Arial', 10, 'bold'),
                   bg='#003153',
                   fg='#F1C40F',
                   relief='raised',
                   height=2,
                   width=25)
# header3.grid(row=0, column=0)
header3.pack(side='left', fill='both')

header31 = tk.Label(div5,
                    text='Carpeta',
                    font=('Arial', 10, 'bold'),
                    bg='#003153',
                    fg='#F1C40F',
                    justify='center',
                    relief='raised',
                    height=2,
                    width=45)
# header31.grid(row=0, column=1)
header31.pack(side='left', fill='both', expand=True)

#+++++++++++++++++++++++++       Dataframe    +++++++++++++++++++++++++#

div6 = tk.LabelFrame(root,
                     bg='#003153',
                     relief='flat')
div6.pack(fill='both', padx=10, expand=True)

mycanvas = tk.Canvas(div6, bg='#003153', relief='flat')
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

myframe = tk.Frame(mycanvas, bg='#003153', relief='flat')
mycanvas.create_window((0, 0), window=myframe, anchor='nw')

for n, val in enumerate(commands.brief(), 2):
    data1 = tk.StringVar()
    data1.set(val[0])
    webent = tk.Entry(myframe,
                      textvariable=data1,
                      font=('Arial', 11, 'bold'),
                      bg='#003153',
                      foreground='white',
                      width=25)
    webent.grid(row=n, column=0, sticky='ew', pady=5)
    
    data2 = tk.StringVar()
    data2.set(val[1])
    webent2 = tk.Entry(myframe,
                      textvariable=data2,
                      font=('Arial', 11, 'bold'),
                      bg='#003153',
                      foreground='white',
                      width=74)
    webent2.grid(row=n, column=1, sticky='ew')
    
    # citykey = tk.Label(myframe,
    #                    text=val[0] + '   :',
    #                    font=('Arial', 11, 'bold'),
    #                    bg='#003153',
    #                    foreground='white',
    #                    padx=30,
    #                    relief='sunken',
    #                    height=2)
    # citykey.grid(row=n, column=0, sticky='ew')

    # pathkey = tk.Label(myframe,
    #                    text=val[1],
    #                    font=('Arial', 11),
    #                    bg='#003153',
    #                    foreground='white',
    #                    padx=90,
    #                    relief='sunken',
    #                    height=2,
    #                    width=45)
    # pathkey.grid(row=n, column=1, sticky='ew')


######################       Separator    ##########################

div8 = tk.LabelFrame(root, bg='#002366', height=10, relief='flat')
div8.pack(padx=6, fill='x')


root.mainloop()
