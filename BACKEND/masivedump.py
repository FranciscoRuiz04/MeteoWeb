# def dbAttributes(pathfile, sep=None, headers=False, iloc=[1, 2], encod='utf-8'):
#     """
#     Get attributes from a csv file for every new record to be added into 
#     cities forecasted database.
#     CSV file must have 2 columns at least: one with the url and another one
#     with the save targetpath where will be saved the data scrapped from the
#     web.

#     Parameters:
#     <<pathfile>> a string with the file path.
    
#     <<sep>> character which separate every field. Is not define by default.

#     <<headers>> indicates if the file have headers. By default is False.

#     <<iloc>> is a list type object with the column number where is every
#     corresponding attribute. The order of indexes corresponds as follow:
#     [url, folder, name]. By default takes the order [1, 2].
#     For example:
#     [2,1] indicates that url is in the second column and the targetpath folder
#     information is in the column number one. 
    
#     <<encod>> File encoding. By defaul is UTF-8.

#     """

#     attributes = {}
    
#     with open(pathfile, 'r', encoding=encod) as file:
#         lines = (line.split(sep) for line in file)
#         if headers:
#             next(lines)
#         for line in lines:
#             atts = [att.strip("\n\ufeff") for att in line]
            
#             attributes['url'] = atts[iloc[0]-1]
#             attributes['name'] = atts[iloc[1]-1]
#             yield attributes


# if __name__ == '__main__':
#     print(next(dbAttributes('c:/users/francisco ruiz/desktop/example2.txt', encod='utf-8', sep='\t')))

# Import Tkinter library
from tkinter import *

# Create an instance of tkinter frame
win = Tk()

# Set the geometry of Tkinter frame
win.geometry("700x250")

# Define Function to print the input value
def display_input():
    if var1.get():
        var2 = 0
    elif var2.get():
        var1 = 0
    print("Input for Python:", var1.get())
    print("Input for C++:", var2.get())

# Define empty variables
var1 = IntVar()
var2 = IntVar()

# Define a Checkbox
t1 = Checkbutton(win, text="Python", variable=var1, onvalue=1, offvalue=0, command=display_input)
t1.pack()
t2 = Checkbutton(win, text="C++", variable=var2, onvalue=1, offvalue=0, command=display_input)
t2.pack()

win.mainloop()