import numpy as np
from random import randint, choice, random

from TP_Investigacion_Fractales.ImagenHelper import directions, angles, get_transformed


class Transformacion:
    def __init__(self, i: int, j: int, x: int, y: int, dir: int, ang: int, contrast, brightness, d, s):
        self.X = x
        self.Y = y
        self.I = i
        self.J = j
        self.IsometricFlip = dir, ang
        self.Contrast = contrast
        self.Brightness = brightness
        self.D = d
        self.S = s

    def GetDistancia(self):
        S = self.Contrast * self.S + self.Brightness
        return np.sum(np.square(self.D - S))

    def Mutar(self, img, step, source_size, factor):
        numeroParametro = randint(1, 4)
        if numeroParametro == 1:
            self.IsometricFlip = choice(directions), self.IsometricFlip[1]
        elif numeroParametro == 2:
            self.IsometricFlip = self.IsometricFlip[0], choice(angles)
        elif numeroParametro == 3:
            self.Brightness = self.Brightness + random()
        elif numeroParametro == 4:
            self.Contrast = self.Contrast + random()
        tranformation = get_transformed(img, self.X, self.Y, self.IsometricFlip[0], self.IsometricFlip[1], step,
                                        source_size, factor)
        self.S = tranformation[4]
