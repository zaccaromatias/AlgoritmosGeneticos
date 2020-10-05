from Ejercicio1.PorcionRuleta import PorcionRuleta


# Representa a un cromosoma con su valor, si es marcado como elite
# y la porcion de ruleta que ocuparia en una poblacion y su fitness
class Cromosoma:
    def __init__(self, x, y, flip, o, s):
        self.X = x
        self.Y = y
        self.Flip = flip
        self.Contrast = o
        self.Scaling = s
        self.EsElite = False
        self.PorcionRuleta = PorcionRuleta()

        # Resetea valores

    def Reset(self):
        self.PorcionRuleta = PorcionRuleta()
        self.EsElite = False

    # Marca cromosoma que es elite
    def Elite(self):
        self.EsElite = True

    # cambia valor del cromosoma
    def Mutar(self, valor):
        self.X = valor

    # Devuelve una instancia nueva pero con mismos valores
    # Para evitar valores por referencia
    def Clone(self):
        cromosoma = Cromosoma(self.X, self.Y, self.Flip, self.Contrast, self.Scaling)
        cromosoma.EsElite = self.EsElite
        cromosoma.PorcionRuleta = self.PorcionRuleta
        return cromosoma
