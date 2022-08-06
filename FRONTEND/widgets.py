__author__ = "Ulises Francisco Ruiz Gomez"
__copyright__ = "Copyright 2022, GPS"
__credits__ = "GPS"

__version__ = "1.0.1"
__maintainer__ = "Francisco Ruiz"
__email__ = "franciscoruiz078@gmail.com"
__status__ = "Developer"


######################       Packages    ##########################

import tkinter as tk
from tkinter import filedialog
#--------------------------------------------------------------#


def _browseFiles(var):
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text Files",
                                                      "*.csv;*.txt"),))
    # Change label contents
    var.set(filename)


def _browseDir(var):
    path = filedialog.askdirectory(initialdir="/",
                                   title="Select a File")
    var.set(path)


def checkBx(curval, *others):
    if curval:
        for val in others:
            val.deselect()


class CB(tk.Checkbutton):
    def __init__(self, div, text, functionality=None, variable=None):
        tk.Checkbutton.__init__(self, div, text=text, variable=variable, onvalue=1,
                                offvalue=0, command=functionality, background='#134351',
                                font=('Arial', 10, 'bold'), activebackground='#134351', fg='#dcdcdc',
                                height=2, selectcolor='#818284')


class LabelFrame(tk.LabelFrame):
    def __init__(self, root, height=None, bg='#134351'):
        tk.LabelFrame.__init__(
            self, master=root, bg=bg, relief='flat', height=height)


class SectionName(tk.Label):
    def __init__(self, div, text):
        tk.Label.__init__(self, master=div, text=text, font=(
            'Arial', 9, 'bold'), bg='#134351', fg='#FFBD08')


class EntryName(tk.Label):
    def __init__(self, div, text, relief=None, height=None, width=None, anchor=None):
        tk.Label.__init__(self, master=div, text=text, font=(
            'Arial', 10, 'bold'), bg='#134351', fg='#dcdcdc', padx=10, relief=relief, height=height, width=width, anchor=anchor,)


class Entry(tk.Entry):
    def __init__(self, div, wd=75, text=None, isbold=False):
        if isbold:
            font = ('Arial', 10, 'bold')
        else:
            font = ('Arial', 10)
        tk.Entry.__init__(self, master=div, width=wd, font=font, borderwidth=3,
                          exportselection=True, justify='center', bg='#dcdcdc', fg='black', textvariable=text)


class Button(tk.Button):
    def __init__(self, div, text, functionality=None, htxt=11):
        tk.Button.__init__(self, master=div, text=text, font=('Arial', htxt, 'bold'), border=3,
                           relief='ridge', bg='#134351', fg='#FFBD07', width=8, command=functionality)


class SearchBtm(Button):
    def __init__(self, div, text, variable, forfile=False):
        if forfile:
            def function(): return _browseFiles(variable)
        else:
            def function(): return _browseDir(variable)
        Button.__init__(self, div, text, function, htxt=9)


class MenuBar(tk.Menu):
    def __init__(self, root):
        tk.Menu.__init__(self, root, bg='#134351', tearoff=0, activebackground='#134351', font=(
            'Arial', 9), fg='#dcdcdc', type='tearoff', activeforeground='#FFBD07')
