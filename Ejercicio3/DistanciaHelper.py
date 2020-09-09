from pandas import DataFrame
import numpy as np

from Ejercicio3.Capital import Capital
from itertools import islice
from openpyxl import load_workbook


class DistanciaHelper:
    TablaDistancias = None
    Capitales = []
    Visitadas = np.arange(23)
    @staticmethod
    def LoadTablaDistanicaYCapitales():
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
    def GetDistancia(capitalOrigen: Capital,capitalDestino :Capital) -> int:
        return DistanciaHelper.TablaDistancias[capitalOrigen.Indice, capitalDestino.Indice]

    @staticmethod
    def GetAllCuidad(capital:Capital):
        print("Indice"+("Valor").center(30, " "))
        for cap in capital:
            print(repr(cap.Indice) + repr(cap.Nombre).center(40, " "))

    @staticmethod
    def InicialCuidadVisitado(capital: Capital):
        print("Indice" + ("Valor").center(30, " "))
        for cap in range(len(capital) - 1):
            DistanciaHelper.Visitadas[cap] = 0



