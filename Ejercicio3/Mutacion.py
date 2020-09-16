# Clase meramente informativa para saber las mutaciones realizadas por la aplicacion
class Mutacion:
    def __init__(self, original):
        self.Original = original.Clone()

    def SetMutante(self, mutante, indices):
        self.Mutante = mutante.Clone()
        self.Indices = indices
