# Clase que contiene la parametrizacion basica para ejecutar el programa
class Configuracion:
    def __init__(self, probabilidadCrossover: float, probabilidadMutacion: float, cantidadEnPoblacionInicial: int,
                 iteraciones: int, elite: bool, diversidadGenetica: bool):
        self.ProbabilidadCrossover = probabilidadCrossover
        self.ProbabilidadMutacion = probabilidadMutacion
        self.ProbabilidadMutacionOriginal = probabilidadMutacion
        self.CantidadPoblacionInicial = cantidadEnPoblacionInicial
        self.Iteraciones = iteraciones
        self.Elite = elite
        self.DiversidadGenetica = diversidadGenetica
