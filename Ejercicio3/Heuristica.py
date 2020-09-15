import numpy as np
import matplotlib.pyplot as plt
from Ejercicio3.DistanciaHelper import DistanciaHelper


class Heuristica:

    @staticmethod
    def GetRecorrerCuidad(cuidadpartida: int):
        """Calcula el recorrido con la ciudad elegida como inicial"""
        DistanciaHelper.recorrido[23] = DistanciaHelper.recorrido[0] = cuidadpartida
        cuidadactual = cuidadpartida
        DistanciaHelper.Visitadas[cuidadactual] = 1

        # Busca la siguiente ciudad para agregar a la lista recorrido siendo la elegida la más cercana
        for rec in range(1, len(DistanciaHelper.Capitales) - 1):
            cuidadactual = DistanciaHelper.recorrido[rec] = Heuristica.BuscarCiudad(cuidadactual)
            DistanciaHelper.Visitadas[cuidadactual] = 1

    @staticmethod
    def BuscarCiudad(actual):
        """Busca la ciudad mas cercana a la actual"""
        destino = 0
        menor = 10000
        for cap in range(len(DistanciaHelper.Capitales) - 1):
            # Revisa si cap ya no fue visitada
            if DistanciaHelper.Visitadas[cap] == 0:
                dis = int(
                    DistanciaHelper.GetDistancia(DistanciaHelper.Capitales[actual], DistanciaHelper.Capitales[cap]))
                # Compara la distancia entre capitales y la guarda si es menor a la registrada hasta el momento
                if dis < menor:
                    menor = dis
                    destino = cap
        return destino

    @staticmethod
    def GetOptimo():
        """Busca la ciudad inicial para que el recorrido sea el óptimo, lo calcula y lo muestra"""
        opt = 10000
        capini = 99
        # Calcula los recorridos mínimos con cada capital como inicial
        for cap in range(len(DistanciaHelper.Capitales) - 1):
            DistanciaHelper.InicialCiudadVisitada()
            Heuristica.GetRecorrerCuidad(cap)
            capacum = 0
            """Cantidad de KM recorridos"""
            for km in range(len(DistanciaHelper.Capitales) - 1):
                capacum += int(DistanciaHelper.GetDistancia(DistanciaHelper.Capitales[DistanciaHelper.recorrido[km]],
                                                            DistanciaHelper.Capitales[DistanciaHelper.recorrido[km + 1]]))
            # Compara para buscar el recorrido óptimo
            if capacum <= opt:
                opt = capacum
                capini = cap
        print("El recorrido óptimo comienza en: ", DistanciaHelper.Capitales[capini].Nombre)
        # Vuelve a calcular el recorrido óptimo para mostrarlo en pantalla
        DistanciaHelper.InicialCiudadVisitada()
        Heuristica.GetRecorrerCuidad(capini)
        Heuristica.PrintRecorrido()

    @staticmethod
    def PrintRecorrido():
        """Muestra el recorrido en pantalla junto con la distancia total calculada en KM"""
        reckm = 0
        print("Indice" + "Ciudad".center(30, " "))
        for rec in range(len(DistanciaHelper.recorrido)):
            print(repr(DistanciaHelper.Capitales[DistanciaHelper.recorrido[rec]].Indice) +
                  repr(DistanciaHelper.Capitales[DistanciaHelper.recorrido[rec]].Nombre).center(40, " "))
        for cap in range(len(DistanciaHelper.recorrido) - 1):
            reckm += int(DistanciaHelper.GetDistancia(DistanciaHelper.Capitales[DistanciaHelper.recorrido[cap]],
                                                      DistanciaHelper.Capitales[DistanciaHelper.recorrido[cap + 1]]))
        print("La distancia total recorrida es de " + repr(reckm) + " km")

    @staticmethod
    def DibujarMapa():
        """Traza el recorrido en un mapa de Argentina"""
