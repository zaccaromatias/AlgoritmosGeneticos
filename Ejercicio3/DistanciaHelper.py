from pandas import DataFrame

from Ejercicio3.Capital import Capital
from itertools import islice
from openpyxl import load_workbook


class DistanciaHelper:
    TablaDistancias = None
    Capitales = []

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
        return DistanciaHelper.TablaDistancias[capitalOrigen.indice, capitalDestino.indice]
