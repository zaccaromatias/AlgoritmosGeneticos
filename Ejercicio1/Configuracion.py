class Configuracion:

    def __init__(self, probabilidadCrossover: float, probabilidadMutacion: float, cantidadEnPoblacionInicial: int,
                 iteraciones: int, elite: bool):
        self.ProbabilidadCrossover = probabilidadCrossover
        self.ProbabilidadMutacion = probabilidadMutacion
        self.CantidadPoblacionInicial = cantidadEnPoblacionInicial
        self.Iteraciones = iteraciones
        self.Elite = elite
