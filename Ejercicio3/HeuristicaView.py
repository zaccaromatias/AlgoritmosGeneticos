from tkinter import *
from tkinter import ttk
from Ejercicio3.DistanciaHelper import DistanciaHelper
from Ejercicio3.Heuristica import Heuristica
from Ejercicio3.MapHelper import MapHelper


class HeuristicaViewModel:
    def __init__(self):
        self.CiudadOrigen = StringVar()
        self.DistanciaTotal = StringVar()
        pass


class HeuristicaView(Toplevel):
    def __init__(self, master=None):
        super().__init__(master=master)
        self.title("Configuracion de Algoritmos Genéticos")

        self.geometry("370x250")
        self.resizable(False, False)

        self.Model = HeuristicaViewModel()

        lblCiudadOrigen = Label(self, text="Ciudad origen: ")
        cboCiudadOrigen = ttk.Combobox(self, textvariable=self.Model.CiudadOrigen,
                                       values=DistanciaHelper.Capitales)

        lblDistanciaTotalText = Label(self, text="Distancia Total Km: ")
        lblDistanciaTotalValue = Label(self, textvariable=self.Model.DistanciaTotal)

        btnrun = Button(self, text="Ejecutar", command=lambda: self.Run())

        lblCiudadOrigen.pack()
        lblCiudadOrigen.place(x=20, y=20)
        cboCiudadOrigen.pack()
        cboCiudadOrigen.place(x=150, y=20)

        lblDistanciaTotalText.pack()
        lblDistanciaTotalText.place(x=20, y=50)

        lblDistanciaTotalValue.pack()
        lblDistanciaTotalValue.place(x=150, y=50)

        self.progress = ttk.Progressbar(self, orient=HORIZONTAL,
                                        length=200, mode='determinate')

        btnrun.pack()
        btnrun.place(x=240, y=220)
        self.progress.pack()
        self.progress.place(x=10, y=220)

    def Run(self):
        nombreCiudadOrigen = self.Model.CiudadOrigen.get()
        recorrido = None
        if (nombreCiudadOrigen != ''):
            recorrido = Heuristica.CalcularRecorridoIniciandoEn(
                list(
                    filter(lambda capital: capital.Nombre == nombreCiudadOrigen, DistanciaHelper.Capitales))[
                    0],self)
        else:
            recorrido = Heuristica.CalcularMejorRecorrido(self)
        self.Model.DistanciaTotal.set(DistanciaHelper.GetDistanciaTotal(recorrido))
        MapHelper.DibujarMapa(recorrido)
        self.progress['value'] = 0
        self.update_idletasks()
