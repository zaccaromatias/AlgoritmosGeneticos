import matplotlib.pyplot as plt
from itertools import islice
from openpyxl import load_workbook
from pandas import DataFrame
import pygame as pg
from Ejercicio3.DistanciaHelper import DistanciaHelper


# Leee el valor de las coordenadas de la segunda hoja del excel
# Y agrega todos los puntos  uniendolo con el anteior
class MapHelper:
    # El orden de las coordenadas es igual al de la lista de capitales
    # Después lo paso al Excel
    """
    PosicionCapMapa = [(354, 348), (230, 266), (349, 169), (357, 131), (365, 357),
                       (172, 216), (128, 305), (139, 455), (312, 276), (411, 166),
                       (210, 564), (341, 163), (117, 781), (194, 191), (203, 151),
                       (203, 81), (203, 98), (133, 271), (178, 316), (303, 270),
                       (228, 396), (224, 175), (139, 855), (250, 504)]
    """

    @staticmethod
    def DibujarMapa(recorrido: []):
        wb = load_workbook(filename='TablaCapitales.xlsx')
        ws = wb['Coordenadas']
        data = ws.values
        cols = next(data)[1:]
        data = list(data)
        idx = [r[0] for r in data]
        data = (islice(r, 1, None) for r in data)
        df = DataFrame(data, index=idx, columns=cols)

        pg.init()
        NEGRO = (0, 0, 0)
        BLANCO = (255, 255, 255)
        ROJO = (255, 0, 0)
        VERDE = (10, 150, 30)
        AZUL = (0, 0, 255)
        CAFE = (90, 50, 15)
        CELESTE = (0, 220, 220)
        Dimensiones = (500, 892)
        pg.display.set_caption('Mejor recorrido encontrado')
        mapa = pg.display.set_mode(Dimensiones)
        mapa.fill(CELESTE)
        mapa.blit(pg.image.load('map.png'), (0, 0))
        # pg.draw.line(Pantalla, ROJO, [10, 10], [650, 470], 2)

        for capital in range(len(recorrido) - 1):
            pg.draw.circle(mapa, ROJO, MapHelper.PosicionCapMapa[capital], 4)
        print(df.Long[3])
        print()
        for rec in range(len(recorrido)-1):
            print(recorrido[rec + 1].Indice)
            pg.draw.line(mapa, VERDE, (df.Lat[recorrido[rec].Indice], df.Long[recorrido[rec].Indice]),
                         (df.Lat[recorrido[rec + 1].Indice], df.Long[recorrido[rec + 1].Indice]), 3)
        pg.draw.line(mapa, VERDE, (df.Lat[recorrido[len(recorrido)-1].Indice], df.Long[recorrido[len(recorrido)-1].Indice]),
                     (df.Lat[recorrido[0].Indice], df.Long[recorrido[0].Indice]), 3)
        pg.display.update()

        EXIT = False
        while not EXIT:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    EXIT = True
        pg.quit()


"""
        anterior = None
        fig, ax = plt.subplots(1, figsize=(10, 8))
        ax.set_title(
            'Mapa Argentina - Distancia Recorrida ' + repr(DistanciaHelper.GetDistanciaTotal(recorrido)) + ' Km',
            fontsize=25)
            
        for capital in recorrido:
            # Filtrar por nombre de capital para encontrar la latitud y la longitud de las capitales recorridas
            search = list(filter(lambda cp: cp[0] == capital.Nombre, list(df.iterrows())))
            valname = search[0]
            plt.scatter(valname[1].Lat, valname[1].Long, s=100)
            plt.annotate(valname[0], (valname[1].Lat, valname[1].Long))
            if anterior is not None:
                x_values = [anterior[0], valname[1].Lat]
                y_values = [anterior[1], valname[1].Long]
                line = ax.plot(x_values, y_values, label=valname[0], linestyle='--')
                ax.grid(alpha=0.6)
                line[0].set_linewidth(1)
                line[0].bins = 1
                line[0].set_drawstyle("default")
                anterior = [valname[1].Lat, valname[1].Long]
            else:
                ax.plot(valname[1].Lat, valname[1].Long, label=valname[0], linestyle='--')
                anterior = [valname[1].Lat, valname[1].Long]

            # ax.axis('off')
        plt.legend(fontsize=8, loc="best")
        ax.set_xlabel('Longitud')
        ax.set_ylabel('Latitud')
        plt.show()
"""
