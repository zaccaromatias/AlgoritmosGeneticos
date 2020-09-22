import matplotlib.pyplot as plt
from itertools import islice
from openpyxl import load_workbook
from pandas import DataFrame
import pygame as pg
from Ejercicio3.DistanciaHelper import DistanciaHelper
import time


# Lee el valor de las coordenadas de la segunda hoja del excel
# Y agrega todos los puntos uniendolo con el anterior
class MapHelper:
    @staticmethod
    def DibujarMapa(recorrido: []):
        """Método que dibuja el recorrido recibido como parámetro en un mapa"""
        pg.init()
        NEGRO = (0, 0, 0)
        GRIS = (200, 200, 200)
        BLANCO = (255, 255, 255)
        ROJO = (255, 0, 0)
        CELESTE = (0, 255, 100)
        Dimensiones = (500, 892)
        pg.display.set_caption('Mejor recorrido - ' + repr(DistanciaHelper.GetDistanciaTotal(recorrido)) + ' Km')
        mapa = pg.display.set_mode(Dimensiones)
        mapa.fill(GRIS)
        mapa.blit(pg.image.load('map.png'), (0, 0))
        posicionRefenciasX = 370
        posicionReferenciaY = 470
        font = pg.font.SysFont('calibri', 14)
        font.set_italic(True)
        rectReferencias = pg.Rect(295, 460, 150, 330)
        pg.draw.rect(mapa, BLANCO, rectReferencias)
        pg.draw.line(mapa, NEGRO, (295, 460), (295 + 150, 460), 2)
        pg.draw.line(mapa, NEGRO, (295 + 150, 460), (295 + 150, 460 + 330), 2)
        pg.draw.line(mapa, NEGRO, (295 + 150, 460 + 330), (295, 460 + 330), 2)
        pg.draw.line(mapa, NEGRO, (295, 460 + 330), (295, 460), 2)
        font.set_underline(True)
        text = font.render('Referencias:', True, NEGRO)
        textRect = text.get_rect()
        textRect.center = (posicionRefenciasX, posicionReferenciaY)
        mapa.blit(text, textRect)
        font.set_underline(False)
        pg.display.update()
        font.set_italic(False)
        for indice in range(len(recorrido) - 1):
            pg.draw.circle(mapa, ROJO, (recorrido[indice].Lat, recorrido[indice].Long), 4)
            text = font.render(repr(indice + 1) + ". " + recorrido[indice].Nombre, True, NEGRO)
            textRect = text.get_rect()
            textRect.center = (posicionRefenciasX, posicionReferenciaY+(13*(indice+1)))
            mapa.blit(text, textRect)

        pg.display.update()
        font.set_bold(True)
        for indice in range(len(recorrido) - 1):
            pg.draw.aaline(mapa, CELESTE, (recorrido[indice].Lat, recorrido[indice].Long),
                           (recorrido[indice + 1].Lat, recorrido[indice + 1].Long), 1)
            pg.display.update()
            time.sleep(0.1)

        font.set_bold(True)
        for indice in range(len(recorrido) - 1):
            text = font.render(repr(indice + 1), True, NEGRO)
            textRect = text.get_rect()
            textRect.center = (recorrido[indice].Lat + 8, recorrido[indice].Long - 8)
            mapa.blit(text, textRect)
        pg.display.update()

        EXIT = False
        while not EXIT:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    EXIT = True
        pg.quit()
