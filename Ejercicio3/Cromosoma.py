from Ejercicio3.DistanciaHelper import DistanciaHelper
from Ejercicio3.Mutacion import Mutacion
from Ejercicio3.PorcionRuleta import PorcionRuleta
from random import randint


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

    def Distancia(self):
        return DistanciaHelper.GetDistanciaTotal(self.GetAllCiudades())

    def GetAllCiudades(self):
        copia = self.Ciudades.copy()
        # Agrego Regreso a origen
        copia.append(copia[0])
        return copia

    # cambia valor del cromosoma
    """Cambia de posición dos ciudades entre sí en la lista de ciudades del cromosoma."""

    def Mutar(self) -> Mutacion:
        # El objeto mutacion es solo para datos y saber en una poblaicon cuales fueren mutados
        mutacion = Mutacion(self)
        indiceCiudadACambiar = randint(0, len(self.Ciudades) - 1)
        indiceOtraCiudadACambiar = randint(0, len(self.Ciudades) - 1)
        # Para elegir otro punto que no sea el mismo
        while (indiceCiudadACambiar == indiceOtraCiudadACambiar):
            indiceOtraCiudadACambiar = randint(0, len(self.Ciudades) - 1)
        auxiliar = self.Ciudades[indiceCiudadACambiar]
        self.Ciudades[indiceCiudadACambiar] = self.Ciudades[indiceOtraCiudadACambiar]
        self.Ciudades[indiceOtraCiudadACambiar] = auxiliar
        mutacion.SetMutante(self, [indiceCiudadACambiar, indiceOtraCiudadACambiar])
        return mutacion

    # Devuelve una instancia nueva pero con mismos valores
    # Para evitar valores por referencia
    def Clone(self):
        cromosoma = Cromosoma(self.Ciudades)
        cromosoma.EsElite = self.EsElite
        cromosoma.PorcionRuleta = self.PorcionRuleta
        cromosoma.Ciudades = self.Ciudades.copy()
        return cromosoma
