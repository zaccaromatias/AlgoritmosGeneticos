import matplotlib.pyplot as plt
from itertools import islice
from openpyxl import load_workbook
from pandas import DataFrame
import pygame as pg
from Ejercicio3.DistanciaHelper import DistanciaHelper
import time


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
        pg.init()
        NEGRO = (0, 0, 0)
        BLANCO = (255, 255, 255)
        ROJO = (255, 0, 0)
        VERDE = (10, 150, 30)
        AZUL = (0, 0, 255)
        CAFE = (90, 50, 15)
        CELESTE = (0, 220, 220)
        Dimensiones = (500, 892)
        pg.display.set_caption('Mejor recorrido - ' + repr(DistanciaHelper.GetDistanciaTotal(recorrido)) + ' Km')
        mapa = pg.display.set_mode(Dimensiones)
        mapa.fill(CELESTE)
        mapa.blit(pg.image.load('map.png'), (0, 0))
        # pg.draw.line(Pantalla, ROJO, [10, 10], [650, 470], 2)
        posicionRefenciasX = 370
        posicionReferenciaY =470
        font = pg.font.Font('freesansbold.ttf', 12)
        text = font.render('- Referencias', True, ROJO)
        textRect = text.get_rect()
        textRect.center = (posicionRefenciasX, posicionReferenciaY)
        mapa.blit(text, textRect)
        pg.display.update()
        for indice in range(len(recorrido) - 1):
            # pg.draw.circle(mapa, ROJO, (recorrido[indice].Lat, recorrido[indice].Long), 4)
            text = font.render(repr(indice + 1) + '.' + recorrido[indice].Nombre, True, ROJO)
            textRect = text.get_rect()
            textRect.center = (recorrido[indice].Lat, recorrido[indice].Long)
            mapa.blit(text, textRect)
            text = font.render(repr(indice + 1) + '.' + recorrido[indice].Nombre, True, ROJO)
            textRect = text.get_rect()
            textRect.center = (posicionRefenciasX, posicionReferenciaY+(13*(indice+1)))
            mapa.blit(text, textRect)

        pg.display.update()
        for indice in range(len(recorrido) - 1):
            pg.draw.line(mapa, VERDE, (recorrido[indice].Lat, recorrido[indice].Long),
                         (recorrido[indice + 1].Lat, recorrido[indice + 1].Long), 3)
            pg.display.update()
            time.sleep(0.1)


        EXIT = False
        while not EXIT:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    EXIT = True
        pg.quit()
