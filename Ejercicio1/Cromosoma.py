from Ejercicio1.PorcionRuleta import PorcionRuleta


class Cromosoma:
    def __init__(self, valor):
        self.Valor = valor
        self.YaSeleccionado = False
        self.Elite = False
        self.PorcionRuleta = PorcionRuleta()

    def Algo(self):
        print(self.Valor)

    def Reset(self):
        self.PorcionRuleta = PorcionRuleta()
        self.Elite = False

    def Elite(self):
        self.Elite = True

    def Mutar(self, valor):
        self.Valor = valor

    def Clone(self):
        cromosoma = Cromosoma(self.Valor)
        cromosoma.YaSeleccionado = False
        cromosoma.PorcionRuleta = self.PorcionRuleta
        return cromosoma
