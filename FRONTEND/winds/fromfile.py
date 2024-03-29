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
import widgets as wdg
import commands
#--------------------------------------------------------------#


def importwind(root):
    # Root window
    root = tk.Toplevel(root)
    root.geometry('550x520')
    root.resizable(False, False)
    root.config(bg='#818284')
    root.title('Carga Masiva')
    root.focus_force()

    ########################    I/O    ########################
    div1 = wdg.LabelFrame(root)
    div1.pack(fill='x', padx=10, pady=10)

    h1 = wdg.SectionName(div1, 'Ubicación')
    h1.grid(row=0, column=0, padx=10, pady=3)

    l1 = wdg.EntryName(div1, 'Entrada')
    l1.grid(row=1, column=0, pady=7)

    pathfile = tk.StringVar()
    i1 = wdg.Entry(div1, 50, pathfile)
    i1.grid(row=1, column=1, sticky='w')

    b1 = wdg.SearchBtm(div1, 'Buscar', pathfile, True)
    b1.grid(row=1, column=2, padx=10)

    l2 = wdg.EntryName(div1, 'Salida')
    l2.grid(row=2, column=0, pady=7)

    targetpath = tk.StringVar()
    i2 = wdg.Entry(div1, 50, targetpath)
    i2.grid(row=2, column=1, sticky='w')

    b2 = wdg.SearchBtm(div1, 'Buscar', targetpath)
    b2.grid(row=2, column=2, padx=10)

    ########################    Separator    ########################
    div3 = wdg.LabelFrame(root, 3)
    div3.pack(padx=6, fill='x')

    ########################    Fields Separator    ########################
    div4 = wdg.LabelFrame(root)
    div4.pack(fill='x', padx=10, pady=10)

    h2 = wdg.SectionName(div4, 'Propiedades del Archivo')
    h2.grid(row=0, column=0, padx=10, pady=3)

    h3 = wdg.EntryName(div4, 'Separador de Campos')
    h3.grid(row=1, column=0, pady=5, columnspan=4, sticky='e')

    # -------------------------   Checkbox   ---------------------------
    # Define empty variables
    iscoma = tk.IntVar()
    istab = tk.IntVar()
    isother = tk.IntVar()

    # Comas
    c1 = wdg.CB(div4, 'Coma', lambda: wdg.checkBx(iscoma, c2, c3), iscoma)
    c1.grid(row=2, column=0, padx=40)

    # Tab
    c2 = wdg.CB(div4, 'Tabulación', lambda: wdg.checkBx(istab, c1, c3), istab)
    c2.grid(row=2, column=1, padx=40)

    # Other
    c3 = wdg.CB(div4, 'Otro:', lambda: wdg.checkBx(isother, c1, c2), isother)
    c3.grid(row=2, column=2, padx=30)
    # Separator Value
    separator = wdg.Entry(div4, 3, isbold=True)
    separator.grid(row=2, column=3)

    ########################    Aditional Info    ########################
    div5 = wdg.LabelFrame(root, 3)
    div5.pack(fill='x', padx=10)
    div6 = wdg.LabelFrame(root)
    div6.pack(fill='x', padx=10, pady=10)

    h4 = wdg.SectionName(div6, 'Información Adicional')
    h4.grid(row=0, column=0, padx=10, pady=3, sticky='w')

    ######################    Fields Numeration    #####################
    h5 = wdg.EntryName(div6, text='Numeración de Campos', width=59, anchor='e')
    h5.grid(row=1, pady=10, columnspan=4, sticky='e')
    # # #-------------------------   URL   ---------------------------
    l3 = wdg.EntryName(div6, 'URL:')
    l3.grid(row=2, column=0, sticky='e')
    urlFieldNum = wdg.Entry(div6, 3)
    urlFieldNum.grid(row=2, column=1, sticky='w')
    # # # #-------------------------   Name   ---------------------------
    l4 = wdg.EntryName(div6, 'Nombre:')
    l4.grid(row=2, column=2)
    namFieldNum = wdg.Entry(div6, 3)
    namFieldNum.grid(row=2, column=3, sticky='w', pady=10)

    hnul = wdg.EntryName(div6, '', width=59, anchor='e')
    hnul.grid(row=3, column=0, columnspan=4, sticky='e')

    h6 = wdg.EntryName(div6, 'Configuración', width=59, anchor='e')
    h6.grid(row=4, column=0, columnspan=4, sticky='e')

    # # #-------------------------   Encoding   ---------------------------
    l5 = wdg.EntryName(div6, 'Codificación:')
    l5.grid(row=5, column=0, sticky='e')
    encodValue = wdg.Entry(div6, 8)
    encodValue.grid(row=5, column=1, sticky='w')

    ishead = tk.IntVar()
    cishead = wdg.CB(div6, 'Encabezados', variable=ishead)
    cishead.grid(row=5, column=2, columnspan=2)

    ######################    Run Program    #####################
    sendBtm = wdg.Button(root, 'Listo',
                         lambda: commands.masiveAddCommand(pathfile.get(), targetpath.get(),
                                                           [iscoma.get(), istab.get(
                                                           ), isother.get()],
                                                           separator.get(), encodValue.get(), ishead.get(),
                                                           [urlFieldNum.get(), namFieldNum.get()]))
    sendBtm.pack()

    # root.mainloop()
