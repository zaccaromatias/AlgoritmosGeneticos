from TP_Investigacion_Fractales.PorcionRuleta import PorcionRuleta


# Representa a un cromosoma con su valor, si es marcado como elite
# y la porcion de ruleta que ocuparia en una poblacion y su fitness
class Cromosoma:
    def __init__(self, x: int, y: int, dir: int, ang: int):
        self.X = x
        self.Y = y
        self.RangeX = 0
        self.RangeY = 0
        self.IsometricFlip = dir, ang
        self.Contrast = 0.0
        self.Brightness = 0.0
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
        cromosoma = Cromosoma(self.X, self.Y, self.IsometricFlip[0], self.IsometricFlip[1])
        cromosoma.Contrast = self.Contrast
        cromosoma.Brightness = self.Brightness
        cromosoma.EsElite = self.EsElite
        cromosoma.PorcionRuleta = self.PorcionRuleta
        cromosoma.RangeX = self.RangeX
        cromosoma.RangeY = self.RangeY
        return cromosoma
