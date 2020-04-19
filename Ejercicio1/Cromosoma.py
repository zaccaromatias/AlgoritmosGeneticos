from Ejercicio1.PorcionRuleta import PorcionRuleta


class Cromosoma:
    def __init__(self, valor):
        self.Valor = valor
        self.YaSeleccionado = False
        self.PorcionRuleta = PorcionRuleta()

    def Algo(self):
        print(self.Valor)

    def Reset(self):
        self.YaSeleccionado = False

    def Seleccionar(self):
        self.YaSeleccionado = True
        return self

    def Mutar(self, valor):
        self.Valor = valor

    def Clone(self):
        cromosoma = Cromosoma(self.Valor)
        cromosoma.YaSeleccionado = False
        cromosoma.PorcionRuleta = self.PorcionRuleta
        return cromosoma
