# Clase que contiene la parametrizacion basica para ejecutar el programa
class Configuracion:
    def __init__(self, probabilidadCrossover: float, probabilidadMutacion: float, cantidadEnPoblacionInicial: int,
                 iteraciones: int, elite: bool, color: bool):
        self.ProbabilidadCrossover = probabilidadCrossover
        self.ProbabilidadMutacion = probabilidadMutacion
        self.ProbabilidadMutacionOriginal = probabilidadMutacion
        self.CantidadPoblacionInicial = cantidadEnPoblacionInicial
        self.SourceBlockSize = 8
        self.Iteraciones = iteraciones
        self.Elite = elite
        # self.DiversidadGenetica = diversidadGenetica
        self.IsRGB = color
