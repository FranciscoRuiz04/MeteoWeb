from textwrap import fill
import tkinter as tk
from tkinter.messagebox import showinfo


# Root window
root = tk.Tk()
root.geometry('850x450')
root.resizable(False, False)
root.config(bg='#000000')
root.title('MeteoWeb')


######################       New Location    ##########################
div1 = tk.LabelFrame(root,
                     bg='#303030',
                     relief='flat')
div1.pack(fill='x', padx=10, pady=10)

header1 = tk.Label(div1,
                   text='Nueva locación',
                   font=('Arial', 10, 'bold'),
                   bg='#303030',
                   fg='#F1C40F')
header1.grid(row=0, column=0, padx=10, pady=3)

# URL
urlLab = tk.Label(div1,
                  text='URL',
                  font=('Arial', 11, 'bold'),
                  bg='#303030',
                  foreground='white',
                  padx=10)
urlLab.grid(row=1, column=0, pady=7)

ent = tk.Entry(div1, width=75, font=('Arial', 12),
               borderwidth=3,
               exportselection=True,
               justify='center',
               bg='white', fg='black')
ent.grid(row=1, column=1)

# Target Path
targetLab = tk.Label(div1,
                     text='Carpeta',
                     font=('Arial', 11, 'bold'),
                     bg='#303030',
                     foreground='white',
                     padx=10)
targetLab.grid(row=2, column=0, pady=7)

ent2 = tk.Entry(div1, width=75, font=('Arial', 12),
                borderwidth=3,
                exportselection=True,
                justify='center',
                bg='white', fg='black')
ent2.grid(row=2, column=1)

# Cityname
cityLab = tk.Label(div1,
                   text='Nombre',
                   font=('Arial', 11, 'bold'),
                   bg='#303030',
                   foreground='white',
                   padx=10)
cityLab.grid(row=3, column=0, pady=7)

ent3 = tk.Entry(div1, width=75, font=('Arial', 12),
                borderwidth=3,
                exportselection=True,
                justify='center',
                bg='white', fg='black')
ent3.grid(row=3, column=1)

# Add bottom
btn1 = tk.Button(div1,
                 text='Añadir',
                 font=('Arial', 12, 'bold'),
                 border=3,
                 relief='ridge',
                 bg='#000000',
                 fg='#F1C40F',
                 width=10)
btn1.grid(row=4, column=1, pady=15)


######################       Separator    ##########################

div2 = tk.LabelFrame(root, bg='#F1C40F', height=3, relief='flat')
div2.pack(padx=6, fill='x')


######################       Drop Location    ##########################
div3 = tk.LabelFrame(root,
                     bg='#303030',
                     relief='flat')
div3.pack(fill='x', padx=10, pady=10)

header2 = tk.Label(div3,
                   text='Borrar Locación',
                   font=('Arial', 10, 'bold'),
                   bg='#303030',
                   fg='#F1C40F')
header2.grid(row=0, column=0, padx=10, pady=3)

# Cityname
namLab = tk.Label(div3,
                  text='Nombre',
                  font=('Arial', 11, 'bold'),
                  bg='#303030',
                  foreground='white',
                  padx=10)
namLab.grid(row=1, column=0, pady=7)

ent3 = tk.Entry(div3,
                width=75,
                font=('Arial', 12),
                borderwidth=3,
                exportselection=True,
                justify='center',
                bg='white', fg='black')
ent3.grid(row=1, column=1)

# Delete bottom
btn2 = tk.Button(div3,
                 text='Borrar',
                 font=('Arial', 12, 'bold'),
                 border=3,
                 relief='ridge',
                 bg='#000000',
                 fg='#F1C40F',
                 width=10)
btn2.grid(row=4, column=1, pady=15)


######################       Separator    ##########################

div4 = tk.LabelFrame(root, bg='#F1C40F', height=3, relief='flat')
div4.pack(padx=6, fill='x')


######################       Content Brief    ##########################

div5 = tk.LabelFrame(root,
                     bg='#303030',
                     relief='flat')
div5.pack(fill='x', padx=10, pady=10)

header3 = tk.Label(div5,
                   text='Resumen',
                   font=('Arial', 10, 'bold'),
                   bg='#303030',
                   fg='#F1C40F')
header3.grid(row=0, padx=10, pady=3)


root.mainloop()
