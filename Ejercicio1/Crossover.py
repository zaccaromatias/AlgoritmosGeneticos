from Ejercicio1.Cromosoma import Cromosoma


class Crossover:
    def __init__(self, projenitor1: Cromosoma, projenitor2: Cromosoma, hijo1: Cromosoma,
                 hijo2: Cromosoma, unidades: int):
        self.Projenitor1 = projenitor1
        self.Projenitor2 = projenitor2
        self.Hijo1 = hijo1
        self.Hijo2 = hijo2
        self.Unidades = unidades

    def MyPrint(self):
        print(
            "//Projenitor1: " + str(int(self.Projenitor1.Valor, 2)) + " --Binario : " + self.Projenitor1.Valor)
        print(
            "//Projenitor2: " + str(int(self.Projenitor2.Valor)) + " --Binario : " + self.Projenitor2.Valor)
        print(
            "//Hijo1: " + str(int(self.Hijo1.Valor)) + " --Binario : " + self.Hijo1.Valor)
        print(
            "//Hijo2: " + str(int(self.Hijo2.Valor)) + " --Binario : " + self.Hijo2.Valor)
        print("//Unidades: " + str(self.Unidades))
