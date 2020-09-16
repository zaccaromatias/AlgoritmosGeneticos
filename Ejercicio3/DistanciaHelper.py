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
        wb = load_workbook(filename='TablaCapitales.xlsx')
        ws = wb['Sheet1']
        data = ws.values
        cols = next(data)[1:]
        data = list(data)
        idx = [r[0] for r in data]
        data = (islice(r, 1, None) for r in data)
        df = DataFrame(data, index=idx, columns=cols)
        DistanciaHelper.TablaDistancias = df.values
        indice = 0
        for columna in cols:
            DistanciaHelper.Capitales.append(Capital(columna, indice))
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
        """Devolucion de todas las ciudades"""
        print("Indice" + "Valor".center(30, " "))
        for cap in DistanciaHelper.Capitales:
            print(repr(cap.Indice) + repr(cap.Nombre).center(40, " "))

    @staticmethod
    def GetDistanciaTotal(capitales: []) -> int:
        distanciaTotal = 0
        for i in range(len(capitales)):
            if ((i + 1) == len(capitales)):
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