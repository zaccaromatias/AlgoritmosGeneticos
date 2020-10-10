# Clase que contiene la parametrizacion basica para ejecutar el programa
class Configuracion:
    def __init__(self, probabilidadCrossover: float, probabilidadMutacion: float, cantElite: int, bloques: int,
                 compresion: float, iteraciones: int, elite: bool, color: bool):
        self.ProbabilidadCrossover = probabilidadCrossover
        self.ProbabilidadMutacion = probabilidadMutacion
        self.ProbabilidadMutacionOriginal = probabilidadMutacion
        self.SourceBlockSize = bloques
        self.CantidadPoblacionInicial = pow(self.SourceBlockSize, 2)
        self.CantElite = cantElite
        self.Compresion = int(1//(1-compresion))
        self.Iteraciones = iteraciones
        self.Elite = elite
        # self.DiversidadGenetica = diversidadGenetica
        self.IsRGB = color
