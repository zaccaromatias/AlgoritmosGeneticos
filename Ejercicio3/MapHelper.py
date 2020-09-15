import matplotlib.pyplot as plt
from itertools import islice
from openpyxl import load_workbook
from pandas import DataFrame
from Ejercicio3.DistanciaHelper import DistanciaHelper


# Esto es un ejemplo de prueba no mas. REFACTORIZAR
# Leee el valor de las coordenadas de la segunda hoja del excel
# Y agrega todos los puntos  uniendolo con el anteior
class MapHelper:
    @staticmethod
    def DibujarMapa():
        wb = load_workbook(filename='TablaCapitales.xlsx')
        ws = wb['Coordenadas']
        data = ws.values
        cols = next(data)[1:]
        data = list(data)
        idx = [r[0] for r in data]
        data = (islice(r, 1, None) for r in data)
        df = DataFrame(data, index=idx, columns=cols)

        indice = 0
        anterior = None
        fig , ax = plt.subplots(1 ,figsize = (10,8))
        ax.set_title('Mapa Argentina', fontsize = 25)
        indexrecorrido = 0
        for value in range(len(DistanciaHelper.recorrido)):
            capital = DistanciaHelper.Capitales[DistanciaHelper.recorrido[value]]
            search = list(filter(lambda cp: cp[0] == capital.Nombre, list(df.iterrows())))
            valname = search[0]
            plt.scatter(valname[1].Lat, valname[1].Long, s=100)
            plt.annotate(valname[0], (valname[1].Lat, valname[1].Long))
            if (anterior != None):
                x_values = [anterior[0], valname[1].Lat]
                y_values = [anterior[1], valname[1].Long]
                line = ax.plot(x_values, y_values, label=valname[0],linestyle='--')
                ax.grid(alpha = 0.6)
                line[0].set_linewidth(1)
                line[0].bins = 1
                line[0].set_drawstyle("default")
                anterior = [valname[1].Lat, valname[1].Long]
            else:
                ax.plot(valname[1].Lat, valname[1].Long, label=valname[0], linestyle='--')
                anterior = [valname[1].Lat, valname[1].Long]
            indice += 1
            #ax.axis('off')
        plt.legend(fontsize = 8,loc="best")
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        plt.show()
