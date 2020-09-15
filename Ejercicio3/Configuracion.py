# Clase que contiene la parametrizacion basica para ejecutar el programa
class Configuracion:
    def __init__(self, probabilidadCrossover: float, probabilidadMutacion: float, ciudadInicial: int,
                 iteraciones: int, elite: bool, diversidadGenetica: bool):
        self.ProbabilidadCrossover = 0.25  # probabilidadCrossover
        self.ProbabilidadMutacion = 0.05  # probabilidadMutacion
        self.ProbabilidadMutacionOriginal = 0.05  # probabilidadMutacion
        self.CiudadInicial = ciudadInicial
        self.NumeroCromosomasPoblacion = 50
        self.Iteraciones = 200  # iteraciones
        self.Elite = True  # elite
        self.DiversidadGenetica = False  # diversidadGenetica
        self.CantidadElites = 2
