from tkinter import *

from TP_Investigacion_Fractales.AlgoritmoGeneticoView import AlgoritmoGeneticoView
from TP_Investigacion_Fractales.CompresionHeuristica import test_greyscale
from TP_Investigacion_Fractales.Configuracion import ConfigurationViewModel


class ProgramView:
    def __init__(self):
        self.top = Tk()
        self.top.wm_title("Aplicacion de Fractales - Compresion de Imagenes")
        self.top.wm_geometry("370x250")
        self.top.resizable(False, False)
        # self.top.eval('tk::PlaceWindow . center')

    def RunHeuristica(self):
        test_greyscale(ConfigurationViewModel().ToConfiguration())

    def ShowAlgoritmoGeneticoConfigurationView(self):
        AlgoritmoGeneticoView(self.top)

    def Show(self):
        btnHeuristica = Button(self.top, text="Heuristica", command=lambda: self.RunHeuristica())
        btnAlgoritmoGenetico = Button(self.top, text="Algoritmos Geneticos",
                                      command=lambda: self.ShowAlgoritmoGeneticoConfigurationView())

        btnHeuristica.pack()
        btnHeuristica.place(x=80, y=83)

        btnAlgoritmoGenetico.pack()
        btnAlgoritmoGenetico.place(x=200, y=83)

        self.top.mainloop()


if __name__ == '__main__':
    ProgramView().Show()
