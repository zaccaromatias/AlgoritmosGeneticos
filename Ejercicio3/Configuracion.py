# Clase que contiene la parametrizacion basica para ejecutar el programa
import tkinter as tk


class Configuracion:
    def __init__(self, probabilidadCrossover: float, probabilidadMutacion: float,
                 numerosCromosomasPoblacion: int,
                 iteraciones: int, elite: bool, diversidadGenetica: bool, cantidadElites: int):
        self.ProbabilidadCrossover = probabilidadCrossover
        self.ProbabilidadMutacion = probabilidadMutacion
        self.NumeroCromosomasPoblacion = numerosCromosomasPoblacion
        self.Iteraciones = iteraciones
        self.Elite = elite
        self.DiversidadGenetica = diversidadGenetica
        self.CantidadElites = cantidadElites


class ConfigurationViewModel:
    def __init__(self):
        self.ProbabilidadCrossover = tk.StringVar(value=0.75)
        self.ProbabilidadMutacion = tk.StringVar(value=0.05)
        self.CiudadInicial = tk.StringVar(value=None)
        self.NumeroCromosomasPoblacion = tk.StringVar(value=50)
        self.Iteraciones = tk.StringVar(value=100)
        self.Elite = tk.BooleanVar(value=False)  # elite
        self.DiversidadGenetica = tk.BooleanVar(value=False)
        self.CantidadElites = tk.StringVar(value=2)

    def ToConfiguration(self) -> Configuracion:
        return Configuracion(probabilidadCrossover=float(self.ProbabilidadCrossover.get()),
                             probabilidadMutacion=float(self.ProbabilidadMutacion.get()),
                             numerosCromosomasPoblacion=int(self.NumeroCromosomasPoblacion.get()),
                             iteraciones=int(self.Iteraciones.get()),
                             elite=bool(self.Elite.get()),
                             diversidadGenetica=bool(self.DiversidadGenetica.get()),
                             cantidadElites=int(self.CantidadElites.get()))
