from Ejercicio3.PorcionRuleta import PorcionRuleta


# Representa a un cromosoma con su valor, si es marcado como elite
# y la porcion de ruleta que ocuparia en una poblacion y su fitness
class Cromosoma:
    def __init__(self, c: list):
        self.EsElite = False
        self.PorcionRuleta = PorcionRuleta()
        self.Ciudades = c.copy()

        # Resetea valores

    def Reset(self):
        self.PorcionRuleta = PorcionRuleta()
        self.EsElite = False

    # Marca cromosoma que es elite
    def Elite(self):
        self.EsElite = True

    # cambia valor del cromosoma
    def Mutar(self):
        pass

    # Devuelve una instancia nueva pero con mismos valores
    # Para evitar valores por referencia
    def Clone(self):
        cromosoma = Cromosoma(self.Valor)
        cromosoma.EsElite = self.EsElite
        cromosoma.PorcionRuleta = self.PorcionRuleta
        cromosoma.Ciudades = self.Ciudades
        return cromosoma
