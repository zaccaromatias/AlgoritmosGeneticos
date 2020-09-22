from pandas import DataFrame
import numpy as np

from Ejercicio3.Capital import Capital
from itertools import islice
from openpyxl import load_workbook


class DistanciaHelper:
    TablaDistancias = None
    """Arreglo que contiene las distancias entre capitales"""
    Capitales = []

    @staticmethod
    def LoadTablaDistanciaYCapitales():
        """Lee desde Excel la tabla de ciudades y distancias e inicializa con ella TablaDistancias y Capitales"""
        workbook = load_workbook(filename='TablaCapitales.xlsx')
        worksheetdistancia = workbook['Sheet1']
        datadistancia = worksheetdistancia.values
        columnasdistancia = next(datadistancia)[1:]
        datadistancia = list(datadistancia)
        idxdistancia = [r[0] for r in datadistancia]
        datadistancia = (islice(r, 1, None) for r in datadistancia)
        dataframedistancia = DataFrame(datadistancia, index=idxdistancia, columns=columnasdistancia)
        DistanciaHelper.TablaDistancias = dataframedistancia.values
        indice = 0

        worksheetcoordenadas = workbook['Coordenadas']
        datacoordenadas = worksheetcoordenadas.values
        columnascoordenadas = next(datacoordenadas)[1:]
        datacoordenadas = list(datacoordenadas)
        idxcoordenadas = [r[0] for r in datacoordenadas]
        datacoordenadas = (islice(r, 1, None) for r in datacoordenadas)
        dataframecoordenadas = DataFrame(datacoordenadas, index=idxcoordenadas, columns=columnascoordenadas)

        for columna in columnasdistancia:
            DistanciaHelper.Capitales.append(
                Capital(columna, indice, dataframecoordenadas.Lat[indice], dataframecoordenadas.Long[indice]))
            indice += 1
        pass

    @staticmethod
    def ResetVisitadas():
        for capital in DistanciaHelper.Capitales:
            capital.SetVisitada(False)

    @staticmethod
    def GetDistancia(capitalOrigen: Capital, capitalDestino: Capital) -> int:
        """Devuelve la distancia entre dos ciudades"""
        return int(DistanciaHelper.TablaDistancias[capitalOrigen.Indice, capitalDestino.Indice])

    @staticmethod
    def GetAllCiudades():
        """Devolución de todas las ciudades"""
        print("Indice" + "Valor".center(30, " "))
        for cap in DistanciaHelper.Capitales:
            print(repr(cap.Indice) + repr(cap.Nombre).center(40, " "))

    @staticmethod
    def GetDistanciaTotal(capitales: []) -> int:
        """Calcula la distancia total recorrida"""
        distanciaTotal = 0
        for i in range(len(capitales)):
            if (i + 1) == len(capitales):
                return distanciaTotal
            distanciaTotal += DistanciaHelper.GetDistancia(capitales[i], capitales[i + 1])
        return distanciaTotal

    @staticmethod
    def PrintRecorrido(recorrido: []):
        """Muestra el recorrido en pantalla junto con la distancia total calculada en KM"""
        reckm = 0
        print("Indice" + "Ciudad".center(30, " "))
        for capital in recorrido:
            print(repr(capital.Indice) +
                  repr(capital.Nombre).center(40, " "))

        print("La distancia total recorrida es de " + repr(DistanciaHelper.GetDistanciaTotal(recorrido)) + " km")
