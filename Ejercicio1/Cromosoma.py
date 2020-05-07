from Ejercicio1.PorcionRuleta import PorcionRuleta


class Cromosoma:
    def __init__(self, valor):
        self.Valor = valor
        self.EsElite = False
        self.PorcionRuleta = PorcionRuleta()

    def Algo(self):
        print(self.Valor)

    def Reset(self):
        self.PorcionRuleta = PorcionRuleta()
        self.EsElite = False

    def Elite(self):
        self.EsElite = True

    def Mutar(self, valor):
        self.Valor = valor

    def Clone(self):
        cromosoma = Cromosoma(self.Valor)
        cromosoma.EsElite = self.EsElite
        cromosoma.PorcionRuleta = self.PorcionRuleta
        return cromosoma
