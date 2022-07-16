import tkinter as tk
from tkinter.messagebox import showinfo


root = tk.Tk()
root.geometry('600x50')
root.resizable(False, False)
root.config(bg='#1A237E')
root.title('Forecast')

df = tk.LabelFrame(root, bg='#FBC02D')
df.pack(fill='x', padx=6, pady=6)

lab = tk.Label(df,
               text='URL',
               font=('Arial', 11, 'bold'),
               bg='#FBC02D',
               foreground='#1A237E',
               padx=10)
lab.grid(row=0, column=0)
# Entry Box
ent = tk.Entry(df, width=50,
               font=('Arial', 12),
               borderwidth=3,
               exportselection=True,
               justify='center',
               bg='white', fg='black')
ent.grid(row=0, column=1, columnspan=2)


def changEnv():
    inp = 'starturl="' + ent.get() + '"\n'
    with open('.env', 'r') as file:
        ln2del = file.readline()
        content = file.readlines()[0:]

    file = open('.env', 'w')
    file.write(inp)
    for line in content:
        file.write(line)
    file.close()

    mess = f"Before: {ln2del}\nNow: {inp}"
    showinfo(title='Alert', message=mess)


btn1 = tk.Button(df,
                 text='Change',
                 font=('Arial', 11, 'bold'),
                 command=changEnv,
                 border=3,
                 bg='#F9A825',
                 fg='#1A237E')
btn1.grid(row=0, column=3)

root.mainloop()
