from pandas import DataFrame
import numpy as np

from Ejercicio3.Capital import Capital
from itertools import islice
from openpyxl import load_workbook


class DistanciaHelper:
    TablaDistancias = None
    """Arreglo que contiene las distancias entre capitales"""
    Capitales = []
    """Arreglo que contiene datos de todas las capitales (objetos Capital)"""
    Visitadas = np.arange(24)
    """Arreglo para ver que ciudad que fue visitada (==1) o no (==0)"""

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
    def GetDistancia(capitalOrigen: Capital, capitalDestino: Capital) -> int:
        """Devuelve la distancia entre dos ciudades"""
        return DistanciaHelper.TablaDistancias[capitalOrigen.Indice, capitalDestino.Indice]

    @staticmethod
    def GetAllCiudades():
        """Devolucion de todas las ciudades"""
        print("Indice" + "Valor".center(30, " "))
        for cap in DistanciaHelper.Capitales:
            print(repr(cap.Indice) + repr(cap.Nombre).center(40, " "))

    @staticmethod
    def InicialCiudadVisitada():
        """Funcion que da pie a la inicialización de las ciudades (set Visitadas[i]==0)"""
        for cap in range(len(DistanciaHelper.Capitales) - 1):
            DistanciaHelper.Visitadas[cap] = 0
