from tkinter import *
from Ejercicio3.AlgoritmoGeneticoView import AlgoritmoGeneticoView
from Ejercicio3.HeuristicaView import HeuristicaView


class ProgramView:
    def __init__(self):
        self.top = Tk()
        self.top.wm_title("Ejercicio 3 - Viajante")
        self.top.wm_geometry("370x250")
        self.top.resizable(False, False)
        # self.top.eval('tk::PlaceWindow . center')

    def ShowHeuristicaView(self):
        HeuristicaView(self.top)

    def ShowAlgoritmoGeneticoConfigurationView(self):
        AlgoritmoGeneticoView(self.top)

    def Show(self):
        btnHeuristica = Button(self.top, text="Heuristica", command=lambda: self.ShowHeuristicaView())
        btnAlgoritmoGenetico = Button(self.top, text="Algoritmos Geneticos",
                                      command=lambda: self.ShowAlgoritmoGeneticoConfigurationView())

        btnHeuristica.pack()
        btnHeuristica.place(x=80, y=83)

        btnAlgoritmoGenetico.pack()
        btnAlgoritmoGenetico.place(x=200, y=83)

        self.top.mainloop()
