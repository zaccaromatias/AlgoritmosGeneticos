# Clase que contiene la parametrizacion basica para ejecutar el programa
import tkinter as tk


class Configuracion:
    def __init__(self, probabilidadCrossover: float, probabilidadMutacion: float, numeroDeCromosomas: int,
                 cantidadElites: int, bloques: int,
                 iteraciones: int, elite: bool, color: bool, step: int):
        self.ProbabilidadCrossover = probabilidadCrossover
        self.ProbabilidadMutacion = probabilidadMutacion
        self.Source_Size = bloques
        self.CantidadPoblacionInicial = numeroDeCromosomas
        self.Step = step
        self.CantidadElites = cantidadElites
        # self.Compresion = int(1//(1-compresion))
        self.Iteraciones = iteraciones
        self.Elite = elite
        self.IsRGB = color
        self.Destination_Size = 2
        self.ImagePath = 'doly_256.jpg'


class ConfigurationViewModel:
    def __init__(self):
        self.ProbabilidadCrossover = tk.StringVar(value=0.75)
        self.ProbabilidadMutacion = tk.StringVar(value=0.05)
        self.NumeroCromosomasPoblacion = tk.StringVar(value=64)
        self.Iteraciones = tk.StringVar(value=50)
        self.Elite = tk.BooleanVar(value=True)
        self.CantidadElites = tk.StringVar(value=4)
        self.Bloques = tk.StringVar(value=4)
        self.Step = tk.StringVar(value=4)
        self.IsRGB = tk.BooleanVar(value=False)

    def ToConfiguration(self) -> Configuracion:
        return Configuracion(probabilidadCrossover=float(self.ProbabilidadCrossover.get()),
                             probabilidadMutacion=float(self.ProbabilidadMutacion.get()),
                             numeroDeCromosomas=int(self.NumeroCromosomasPoblacion.get()),
                             cantidadElites=int(self.CantidadElites.get()),
                             bloques=int(self.Bloques.get()),
                             iteraciones=int(self.Iteraciones.get()),
                             elite=bool(self.Elite.get()),
                             color=bool(self.IsRGB.get()),
                             step=int(self.Step.get()))
