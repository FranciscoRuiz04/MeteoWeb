import tkinter as tk
import widgets as wdg

root = tk.Tk()
root.geometry('550x600')
root.resizable(False, False)
root.config(bg='#818284')
root.title('MeteoWeb')


########################    I/O    ########################
div1 = wdg.LabelFrame(root)
div1.pack(fill='x', padx=10, pady=10)

h1 = wdg.SectionName(div1, 'Ubicación')
h1.grid(row=0, column=0, padx=10, pady=3)

l1 = wdg.EntryName(div1, 'Entrada')
l1.grid(row=1, column=0, pady=7)

var1 = tk.StringVar()
i1 = wdg.Entry(div1, 50, var1)
i1.grid(row=1, column=1, sticky='w')

b1 = wdg.SearchBtm(div1, 'Buscar', var1, True)
b1.grid(row=1, column=2, padx=10)

l2 = wdg.EntryName(div1, 'Salida')
l2.grid(row=2, column=0, pady=7)

var2 = tk.StringVar()
i2 = wdg.Entry(div1, 50, var2)
i2.grid(row=2, column=1, sticky='w')

b2 = wdg.SearchBtm(div1, 'Buscar', var2)
b2.grid(row=2, column=2, padx=10)


########################    Separator    ########################
div3 = wdg.LabelFrame(root, 3)
div3.pack(padx=6, fill='x')


########################    Fields Separator    ########################
div4 = wdg.LabelFrame(root)
div4.pack(fill='x', padx=10, pady=10)

# # # Define empty variables
# var1 = tk.IntVar()
# var2 = tk.IntVar()

# # # Define a Checkbox
# t1 = tk.Checkbutton(div4, text="Python", variable=var1, onvalue=1, offvalue=0)
# t1.pack()
# t2 = tk.Checkbutton(div4, text="C++", variable=var2, onvalue=1, offvalue=0)
# t2.pack()

root.mainloop()
