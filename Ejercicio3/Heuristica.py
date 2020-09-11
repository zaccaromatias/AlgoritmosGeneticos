import numpy as np
from Ejercicio3.Capital import Capital
from Ejercicio3.DistanciaHelper import DistanciaHelper
class Heuristica:
    CuidadElijida = None
    """Lista de índices de todas las capitales"""
    Distancia = np.array([23, 23])
    """Lista de índices  recorrido de las capitales"""
    recorrido = np.arange(24)

    """Calcular el recorrido de la ciudad elegida"""

    @staticmethod
    def GetRecorrerCuidad(cuidadpartida, capital: Capital):
        posicionactual = 0
        Heuristica.recorrido[23] = Heuristica.recorrido[0] = cuidadpartida
        cuidadactual = cuidadpartida
        DistanciaHelper.Visitadas[cuidadactual] = 1
        """Llenando el recorrido buscando ciudad de más cercanias """

        for rec in range(1, len(capital) - 1):
            search = Heuristica.BuscarCiudad(cuidadactual)
            Heuristica.recorrido[rec] = search
            cuidadactual = Heuristica.recorrido[rec]
            DistanciaHelper.Visitadas[cuidadactual] = 1

    """Busca la ciudad mas cerca distancia a la actual"""

    @staticmethod
    def BuscarCiudad(actual):
        destino = 0
        menor = 10000
        for cap in range(len(DistanciaHelper.Capitales) - 1):
            """Revisando si ya no fue visitada"""
            if DistanciaHelper.Visitadas[cap] == 0:
                dis = int(
                    DistanciaHelper.GetDistancia(DistanciaHelper.Capitales[actual], DistanciaHelper.Capitales[cap]))
                """Compara la distancia encuentrado y va guardando el menor"""
                if dis < menor:
                    menor = dis
                    destino = cap
        return destino

    """Buscando el óptimo entre todas las capitales del pais"""

    @staticmethod
    def GetOptimo(capital: Capital):
        opt = 10000
        capacum = 0
        capini = 99
        """Interacion entre capital el primer for """
        for cap in range(len(capital) - 1):
            DistanciaHelper.InicialCuidadVisitada(capital)
            Heuristica.GetRecorrerCuidad(cap, capital)
            capacum = 0
            """La cantidad KM recorrido """
            for km in range(len(capital) - 1):
                capacum += int(DistanciaHelper.GetDistancia(DistanciaHelper.Capitales[Heuristica.recorrido[km]],
                                                            DistanciaHelper.Capitales[Heuristica.recorrido[km + 1]]))
            """Camparando para buscar el optimo"""
            if capacum <= opt:
                opt = capacum
                capini = cap
        print("El optimo: ", capital[capini].Nombre)
        """Vuelve a inicial las cuidad para poder calcular el recorrido de nuevo cal la capital opt"""
        DistanciaHelper.InicialCuidadVisitada(capital)
        Heuristica.GetRecorrerCuidad(capini, capital)
        Heuristica.PrintRecorrido()

    @staticmethod
    def PrintRecorrido():
        reckm = 0
        print("Indice" + ("Ciudad").center(30, " "))
        print("Indice" + ("Valor").center(30, " "))
        for rec in range(len(Heuristica.recorrido)):
            print(repr(DistanciaHelper.Capitales[Heuristica.recorrido[rec]].Indice) +
                  repr(DistanciaHelper.Capitales[Heuristica.recorrido[rec]].Nombre).center(40, " "))
        for cap in range(len(DistanciaHelper.Capitales) - 1):
            reckm += int(DistanciaHelper.GetDistancia(DistanciaHelper.Capitales[Heuristica.recorrido[cap]],
                                                      DistanciaHelper.Capitales[Heuristica.recorrido[cap + 1]]))
        print("El recorrido total es de " + repr(reckm) + " km")