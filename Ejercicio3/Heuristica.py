import numpy as np
from Ejercicio3.Capital import Capital
from Ejercicio3.DistanciaHelper import DistanciaHelper
class Heuristica:
    CuidadElijida = None
    Distancia = np.array([23, 23])
    recorrido = np.arange(24)

    @staticmethod
    def GetRecorrerCuidad(cuidadpartida, capital: Capital):
        posicionactual = 0
        Heuristica.recorrido[23] = Heuristica.recorrido[0] = cuidadpartida
        cuidadactual = cuidadpartida
        DistanciaHelper.Visitadas[cuidadactual] = 1
        for rec in range(len(capital) - 1):
            search = Heuristica.BuscarCiudad(cuidadactual)
            Heuristica.recorrido[rec] = search
            cuidadactual = Heuristica.recorrido[rec]
            DistanciaHelper.Visitadas[cuidadactual] = 1

    @staticmethod
    def BuscarCiudad(actual):
        destino = 0
        menor = 10000
        for cap in range(len(DistanciaHelper.Capitales) - 1):
            if DistanciaHelper.Visitadas[cap] == 0:
                dis = int(DistanciaHelper.GetDistancia(DistanciaHelper.Capitales[actual], DistanciaHelper.Capitales[cap]))
                if dis < menor:
                    menor = dis
                    destino = cap
        return destino

    @staticmethod
    def PrintRecorrido():
        reckm = 0
        for cap in range(len(DistanciaHelper.Capitales) - 1):
            reckm += int(DistanciaHelper.GetDistancia(DistanciaHelper.Capitales[Heuristica.recorrido[cap]], DistanciaHelper.Capitales[Heuristica.recorrido[cap + 1]]))
        print("El recorrido total es de {0} km", reckm)