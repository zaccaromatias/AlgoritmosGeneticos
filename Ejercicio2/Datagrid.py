from tkinter import *
from tkinter import ttk
class Datagrig:
    pass

def GenerarGrid(items, valhead,text1,text2,greedy):
    root = Tk()
    #El tamaña del grid depende del algoritmo
    if not greedy:
        root.geometry("300x300")
    else:
        root.geometry("450x300")

    
    root.title('El valor maximo que alcanzo entrar en la mochila')
    frame = Frame()
    frame.pack()
    col = ""
    if not greedy:
        col = (1, 2, 3)
    else:
        col = (1, 2, 3, 4)
    tree = ttk.Treeview(frame, columns=col, height=10, show="headings")
    tree.pack(side='left')

    # Formando la cabecera del grid
    if not greedy:
        tree.heading(1, text="Nombre")
        tree.heading(2, text="Precio")
        tree.heading(3, text=valhead)

        tree.column("1", width=90, anchor='c')
        tree.column("2", width=90, anchor='c')
        tree.column("3", width=90, anchor='c')
    else:
        tree.heading(1, text="Nombre")
        tree.heading(2, text="Precio")
        tree.heading(3, text=valhead)
        tree.heading(4, text="Porcion por unidad")

        tree.column("1", width=90, anchor='c')
        tree.column("2", width=90, anchor='c')
        tree.column("3", width=90, anchor='c')
        tree.column("4", width=125, anchor='c')



    sumprice = 0
    sumvolumen = 0

    for val in items:
        if not greedy:
            tree.insert('', 'end', values=(val.name, val.price, val.unit))
        else:
            tree.insert('', 'end', values=(val.name, val.price, val.unit, val.Ratio))
        sumvolumen += val.unit
        sumprice += val.price  # Equivale a sumprice = sumprice + m.price

    lab = ttk.Label(root, wraplength="4i", justify="left", anchor="ne", padding=(10, 2, 20, 6), text=text1+": {}".format( sumvolumen ))
    lab1 = ttk.Label(root, wraplength="4i", justify="left", anchor="ne", padding=(10, 2, 20, 6), text=text2+": ${}".format( sumprice ))

    lab.pack(fill='x')
    lab1.pack(fill='x')
    tree.pack(side='left')
    root.mainloop()
