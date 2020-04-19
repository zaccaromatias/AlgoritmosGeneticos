from Ejercicio1.Cromosoma import Cromosoma


class Mutacion:
    def __init__(self, original: Cromosoma):
        self.Original = original
        self.Mutante = None
        self.IndiceBitCambiado = None

    def MyPrint(self):
        print(
            "//Original: " + str(self.Original.Valor) + " --Binario : " + str(format(self.Original.Valor, "b")))
        print(
            "//Mutante: " + str(self.Mutante.Valor) + " --Binario : " + str(format(self.Mutante.Valor, "b")))
        print("//Indice Cambiado: " + str(self.IndiceBitCambiado))