from tkinter import *
import tkinter as tk
from tkinter import filedialog
import os

from TP_Investigacion_Fractales.AlgoritmoGeneticoView import AlgoritmoGeneticoView
from TP_Investigacion_Fractales.CompresionHeuristica import test_greyscale
from TP_Investigacion_Fractales.Configuracion import ConfigurationViewModel


class ProgramView(Toplevel):
    def __init__(self):
        self.top = Tk()
        self.top.wm_title("Aplicacion de Fractales - Compresion de Imagenes")
        self.top.wm_geometry("370x250")
        self.top.resizable(False, False)
        self.ImagePath = tk.StringVar()
        # self.top.eval('tk::PlaceWindow . center')

    def RunHeuristica(self):
        test_greyscale(ConfigurationViewModel(self.ImagePath.get()).ToConfiguration())

    def ShowAlgoritmoGeneticoConfigurationView(self):
        AlgoritmoGeneticoView(ConfigurationViewModel(self.ImagePath.get()), self.top)

    def OpenFileDialog(self):
        imagepath = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select file",
            filetypes=(("jpeg files", "*.jpg"), ("gif files", "*.gif"), ("all files", "*.*"),))
        self.ImagePath.set(imagepath)

    def Show(self):
        btnHeuristica = Button(self.top, text="Heuristica", command=lambda: self.RunHeuristica())
        btnAlgoritmoGenetico = Button(self.top, text="Algoritmos Geneticos",
                                      command=lambda: self.ShowAlgoritmoGeneticoConfigurationView())

        lblFilePath = Label(self.top, text="Imagen: ")
        txtImage = Entry(self.top, textvariable=self.ImagePath, state='disabled', width=50)

        btnSeleccionarImagen = Button(self.top, text="Cambiar Imagen", command=lambda: self.OpenFileDialog())

        lblFilePath.pack()
        txtImage.pack()
        btnSeleccionarImagen.pack()
        btnHeuristica.pack()
        btnHeuristica.place(x=80, y=83)

        btnAlgoritmoGenetico.pack()
        btnAlgoritmoGenetico.place(x=200, y=83)

        self.top.mainloop()


if __name__ == '__main__':
    ProgramView().Show()
