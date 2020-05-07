from Ejercicio1.Cromosoma import Cromosoma


class Mutacion:
    def __init__(self, original: Cromosoma):
        self.Original = Cromosoma.Clone(original)
        self.Mutante = Cromosoma.Clone(original)
        self.IndiceBitCambiado = None

    def MyPrint(self):
        print(
            "//Original: " + str(int(self.Original.Valor)) + " --Binario : " + self.Original.Valor)
        print(
            "//Mutante: " + str(int(self.Mutante.Valor)) + " --Binario : " + self.Mutante.Valor)
        print("//Indice Cambiado: " + str(self.IndiceBitCambiado))