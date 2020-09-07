from Ejercicio3.Configuracion import Configuracion
from Ejercicio3.AlgoritmoGenetico import AlgoritmoGenetico
from tkinter import *


# ----------------------------------------------------------------------------------------------------
# PARA UTILIZAR ESTA CLASE HAY QUE COMENTAR LAS LINEAS DE PROGRAM EN INIT.PY Y DESCOMENTAR LAS DE GUI
# PARA UTILIZAR ESTA CLASE HAY QUE COMENTAR LAS LINEAS DE PROGRAM EN INIT.PY Y DESCOMENTAR LAS DE GUI
# PARA UTILIZAR ESTA CLASE HAY QUE COMENTAR LAS LINEAS DE PROGRAM EN INIT.PY Y DESCOMENTAR LAS DE GUI
# PARA UTILIZAR ESTA CLASE HAY QUE COMENTAR LAS LINEAS DE PROGRAM EN INIT.PY Y DESCOMENTAR LAS DE GUI
# PARA UTILIZAR ESTA CLASE HAY QUE COMENTAR LAS LINEAS DE PROGRAM EN INIT.PY Y DESCOMENTAR LAS DE GUI
# ----------------------------------------------------------------------------------------------------

# Este método se invoca al hacer click en Ejecutar y se encarga de invocar a los métodos del algoritmo proveyendo
# los parámetros ingresados.
def run(cross: float, mut: float, cantpob: int, itera: int, chkelite: bool, chkdivgen: bool):
    configuracion = Configuracion(cross, mut, cantpob, itera, chkelite, chkdivgen)
    algoritmo = AlgoritmoGenetico(configuracion)
    algoritmo.Run()
    algoritmo.Print()
    algoritmo.ExportToExcel()


class GUI:

    # Se definen las características de la ventana principal.
    def __init__(self):
        self.top = Tk()
        self.top.wm_title("Algoritmos Genéticos - TP1")
        self.top.wm_geometry("370x250")
        self.top.resizable(False, False)
        self.top.eval('tk::PlaceWindow . center')

    # Se define el contenido de la ventana principal, los controles, campos y botones, así como las variables que toman
    # los valores que se ingresan.
    def start(self):  # -> Configuracion:
        cross = StringVar()
        lblcross = Label(self.top, text="Probabilidad de crossover (entre 0 y 1): ")
        txtcross = Entry(self.top, textvariable=cross)
        txtcross.insert(0, 0.75)
        mut = StringVar()
        lblmut = Label(self.top, text="Probabilidad de mutación (entre 0 y 1): ")
        txtmut = Entry(self.top, textvariable=mut)
        txtmut.insert(0, 0.05)
        cantpob = StringVar()
        lblcantpob = Label(self.top, text="Tamaño de población: ")
        txtcantpob = Entry(self.top, textvariable=cantpob)
        txtcantpob.insert(0, 10)
        itera = StringVar()
        lblitera = Label(self.top, text="Cantidad de iteraciones: ")
        txtitera = Entry(self.top, textvariable=itera)
        txtitera.insert(0, 100)
        lblelite = Label(self.top, text="Elitismo")
        elite = BooleanVar()
        chkelite = Checkbutton(self.top, variable=elite, onvalue=True, offvalue=False)
        lbldivgen = Label(self.top, text="Diversidad genética")
        divgen = BooleanVar()
        chkdivgen = Checkbutton(self.top, variable=divgen, onvalue=True, offvalue=False)
        btnrun = Button(self.top, text="Ejecutar", command=lambda: run(float(cross.get()), float(mut.get()),
                                                                       int(cantpob.get()), int(itera.get()),
                                                                       bool(elite.get()), bool(divgen.get())))

        # Se ubican los diferentes elementos de la ventana dentro de ella.
        lblcross.pack()
        lblcross.place(x=10, y=10)
        txtcross.pack()
        txtcross.place(x=230, y=10)
        lblmut.pack()
        lblmut.place(x=10, y=40)
        txtmut.pack()
        txtmut.place(x=230, y=40)
        lblcantpob.pack()
        lblcantpob.place(x=10, y=70)
        txtcantpob.pack()
        txtcantpob.place(x=230, y=70)
        lblitera.pack()
        lblitera.place(x=10, y=100)
        txtitera.pack()
        txtitera.place(x=230, y=100)
        lblelite.pack()
        lblelite.place(x=160, y=130)
        chkelite.pack()
        chkelite.place(x=230, y=130)
        lbldivgen.pack()
        lbldivgen.place(x=100, y=160)
        chkdivgen.pack()
        chkdivgen.place(x=230, y=160)
        btnrun.pack()
        btnrun.place(x=150, y=200)

        self.top.mainloop()
