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
            "//Projenitor1: " + str(self.Projenitor1.Valor) + " --Binario : " + str(format(self.Projenitor1.Valor, "b")))
        print(
            "//Projenitor2: " + str(self.Projenitor2.Valor) + " --Binario : " + str(format(self.Projenitor2.Valor, "b")))
        print(
            "//Hijo1: " + str(self.Hijo1.Valor) + " --Binario : " + str(format(self.Hijo1.Valor, "b")))
        print(
            "//Hijo2: " + str(self.Hijo2.Valor) + " --Binario : " + str(format(self.Hijo2.Valor, "b")))
        print("//Unidades: " + str(self.Unidades))
