import tkinter as tk
from tkinter import filedialog



def browseFiles(var):
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text Files",
                                                      "*.csv;*.txt"),))

    # Change label contents
    var.set(filename)

def browseDir(var):
    path = filedialog.askdirectory(initialdir="/",
                                          title="Select a File")
    var.set(path)



class LabelFrame(tk.LabelFrame):
    def __init__(self, root, height=None, bg='#134351'):
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
    def __init__(self, div, wd=75, text=None):
        tk.Entry.__init__(self, master=div, width=wd, font=(
            'Arial', 10), borderwidth=3, exportselection=True, justify='center', bg='#dcdcdc', fg='black', textvariable=text)


class Button(tk.Button):
    def __init__(self, div, text, functionality, htxt=11):
        tk.Button.__init__(self, master=div, text=text, font=('Arial', htxt, 'bold'), border=3,
                           relief='ridge', bg='#134351', fg='#FFBD07', width=8, command=functionality)


class SearchBtm(Button):
    def __init__(self, div, text, variable, forfile=False):
        if forfile:
            function = lambda: browseFiles(variable)
        else:
            function = lambda: browseDir(variable)
        Button.__init__(self, div, text, function, htxt=9)