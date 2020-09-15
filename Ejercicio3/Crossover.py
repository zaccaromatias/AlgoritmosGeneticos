from Ejercicio3.Cromosoma import Cromosoma


# Clase meramente informativa para saber los corssovers realizados por la aplicacion
class Crossover:
    def __init__(self, projenitor1: Cromosoma, projenitor2: Cromosoma, hijo1: Cromosoma,
                 hijo2: Cromosoma, unidades: int):
        self.Projenitor1 = projenitor1.Clone()
        self.Projenitor2 = projenitor2.Clone()
        self.Hijo1 = hijo1.Clone()
        self.Hijo2 = hijo2.Clone()
        self.Unidades = unidades

    def MyPrint(self):
        print(
            "//Progenitor1: " + str(self.Projenitor1.Distancia()))
        print(
            "//Progenitor2: " + str(self.Projenitor2.Distancia()))
        print(
            "//Hijo1: " + str(self.Hijo1.Distancia()))
        print(
            "//Hijo2: " + str(self.Hijo2.Distancia()))
        print("//Unidades: " + str(self.Unidades))
