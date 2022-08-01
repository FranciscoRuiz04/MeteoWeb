import tkinter as tk
# import sys
# sys.path[0] = sys.path[0][:-9]

class LabelFrame(tk.LabelFrame):
    def __init__(self, root, height=0, bg='#134351'):
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