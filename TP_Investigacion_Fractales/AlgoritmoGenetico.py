# Importamos las funciones para obtener numeros aleatorios
from random import randint, uniform, random, choice
import matplotlib.image as mpimg
from scipy import ndimage
import numpy as np

from TP_Investigacion_Fractales.Cromosoma import Cromosoma
from TP_Investigacion_Fractales.Poblacion import Poblacion


# De la lista de cromosomas que recive devuelve uno tomado al azar
# Simplemente toma un valor entero al azar y devuelve el objeto en ese indice
def SeleccionarCromosomaAlAzar(cromosomas: []) -> Cromosoma:
    numero = randint(0, len(cromosomas) - 1)
    return cromosomas[numero]


def GenerarTransform():
    return choice(angle), choice(direction)


def reduce(img, factor):
    """Reduce el tamaño de la imagen aproximando bloques lindantes"""
    result = np.zeros((img.shape[0] // factor, img.shape[1] // factor))
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            result[i, j] = np.mean(img[i * factor:(i + 1) * factor, j * factor:(j + 1) * factor])
    return result


def IsometricTransform(dirang, img):
    """Genera las contracciones Rt a partir de los bloques Dj."""
    # Rota la imagen según el ángulo dado (sentido antihorario).
    # Invierte la imagen si dirección es -1.
    return ndimage.rotate(img[::dirang[0], :], dirang[1], reshape=False)


direction = [-1, 1]
angle = [0, 90, 180, 270]
"""Coordenadas [x,y] de la esquina superior izquierda de cada bloque del Dominio D"""


# Clase principal de nuestro programa
class AlgoritmoGenetico:

    # Iniciacion de variables, recive el objeto configuracion que contiene la parametrizacion de nuestro programa
    def __init__(self, configuracion):
        self.Configuracion = configuracion
        self.Poblaciones = []
        self.PoblacionActual = []
        self.Image = None

    # Metodo principal que realiza las iteraciones del programa
    def Run(self):
        self.LoadSourceImage(self.Configuracion.IsRGB)
        self.Poblaciones.append(self.GetPoblacionInicial())
        for i in range(self.Configuracion.Iteraciones):
            print('Iteración número ' + str(i + 1))
            self.PoblacionActual = self.Poblaciones[len(self.Poblaciones) - 1]
            # Desmarca e inicializa valores de los cromosomas para evitar valores por referencias y resetear los
            # cromosomas elites
            for cromosoma in self.PoblacionActual.Cromosomas:
                cromosoma.Reset()
            nuevaPoblacion: Poblacion = self.PoblacionActual
            # Realiza la logica de elite si asi se deseo correr
            if self.Configuracion.Elite:
                nuevaPoblacion = self.Elite(nuevaPoblacion)
            nuevaPoblacion = self.SeleccionRuleta(nuevaPoblacion)
            nuevaPoblacion = self.Crossover(nuevaPoblacion)
            self.Mutacion(nuevaPoblacion)
            self.Poblaciones.append(nuevaPoblacion)
        return self.Poblaciones

    def LoadSourceImage(self, RGB: bool):
        if RGB:
            self.Image = mpimg.imread('lena.gif')
        else:
            self.Image = np.mean(mpimg.imread('monkey.gif')[:, :, :2], 2)

    def GetPoblacionInicial(self) -> Poblacion:
        """Genera y devuelve la poblacion inicial dividiendo a la imagen en n bloques del mismo tamaño y guardando
           información relevante a ellos en los cromosomas de dicha población."""
        poblacion = Poblacion()
        for dominioX in range(self.Configuracion.SourceBlockSize):
            for dominioY in range(self.Configuracion.SourceBlockSize):
                SourceBlock = self.Image.shape[0] * dominioX // self.Configuracion.SourceBlockSize, \
                              self.Image.shape[1] * dominioY // self.Configuracion.SourceBlockSize
                dirang = choice(direction), choice(angle)
                c = Cromosoma(SourceBlock[0], SourceBlock[1], dirang[0], dirang[1])
                c.RangeX, c.RangeY, c.Contrast, c.Brightness = self.FindContrastAndBrightness(c, self.Image,
                                                                          self.Configuracion.SourceBlockSize)
                poblacion.Cromosomas.append(c)
        print('Población inicial generada')
        return poblacion

    def FindContrastAndBrightness(self, c: Cromosoma, Image, DominioBlockSize: int):
        # D = Image[c.X:c.X + step, c.Y:c.Y + step]
        compressRatio = DominioBlockSize // self.Configuracion.Compresion
        x = Image.shape[0] - (Image.shape[1] // compressRatio)
        y = Image.shape[1] - (Image.shape[1] // compressRatio)
        randomRangeBlock = randint(0, x), randint(0, y)
        S = Image[randomRangeBlock[0]:randomRangeBlock[0] + Image.shape[0] // compressRatio,
                  randomRangeBlock[1]:randomRangeBlock[1] + Image.shape[1] // compressRatio]
        # S = Image[c.X:c.X + step * 2, c.Y:c.Y + step * 2]
        D = Image[c.X:c.X + Image.shape[0]//DominioBlockSize, c.Y:c.Y + Image.shape[1]//DominioBlockSize]
        S = reduce(S, 2)
        S = IsometricTransform(c.IsometricFlip, S)
        A = np.concatenate((np.ones((S.size, 1)), np.reshape(S, (S.size, 1))), axis=1)
        b = np.reshape(D, (D.size,))
        x, _, _, _ = np.linalg.lstsq(A, b, rcond=None)
        return randomRangeBlock[0], randomRangeBlock[1], x[1], x[0]

    def FuncionObjetivo(self, c: Cromosoma, Image, DominioBlockSize: int):
        """Copiado de la funcion compress() en compression.py"""
        compressRatio = self.Configuracion.SourceBlockSize // self.Configuracion.Compresion
        D = Image[c.RangeX:c.RangeX + compressRatio, c.RangeY:c.RangeY + compressRatio]
        S = Image[c.X:c.X + compressRatio * 2, c.Y:c.Y + compressRatio * 2]
        S = IsometricTransform(c.IsometricFlip, reduce(S, 2))
        S = c.Contrast * S + c.Brightness
        return np.sum(np.square(D - S))

    # Forma de calcular el fitness de cada cromosoma
    # Funcion objetiva de dicho cromosoma sobre la suma la funcion objetivo de cada cromosoma de la poblacion
    def FuncionFitness(self, cromosoma: Cromosoma, img, sourceblocksize: int):
        return 1 / self.FuncionObjetivo(cromosoma, img, sourceblocksize)

    def SeleccionRuleta(self, poblacionInicial: Poblacion) -> Poblacion:
        porciones = []
        nuevaPoblacion = Poblacion()

        elite = list(filter(lambda c: c.EsElite is True, poblacionInicial.Cromosomas))
        for cromosomaElite in elite:
            nuevaPoblacion.Cromosomas.append(cromosomaElite.Clone())

        for cromosoma in poblacionInicial.Cromosomas:
            if len(porciones) == 0:
                valorMinimo = 0
            else:
                valorMinimo = porciones[len(porciones) - 1].ValorMaximo
            valorMaximo = valorMinimo + self.FuncionFitness(cromosoma, self.Image, self.Configuracion.SourceBlockSize)
            cromosoma.PorcionRuleta.ValorMinimo = valorMinimo
            cromosoma.PorcionRuleta.ValorMaximo = valorMaximo
            porciones.append(cromosoma.PorcionRuleta)

        for i in range(self.Configuracion.CantidadPoblacionInicial - len(elite)):
            numero = uniform(0, porciones[len(porciones) - 1].ValorMaximo)
            lista = list(filter(
                lambda c: c.PorcionRuleta.ValorMinimo <= numero < c.PorcionRuleta.ValorMaximo,
                poblacionInicial.Cromosomas))
            nuevaPoblacion.Cromosomas.append(lista[0].Clone())
        return nuevaPoblacion

    def Elite(self, poblacionInicial: Poblacion) -> Poblacion:
        candidates = []
        noElite = list(filter(lambda cd: cd.EsElite is False, poblacionInicial.Cromosomas))
        for cromosoma in noElite:
            fitness = self.FuncionFitness(cromosoma, self.Image, self.Configuracion.SourceBlockSize)
            candidates.append([fitness, cromosoma])
        for i in range(len(candidates)):
            for j in range(0, len(candidates) - i - 1):
                if candidates[j][0] > candidates[j + 1][0]:
                    candidates[j][0], candidates[j + 1][0] = candidates[j + 1][0], candidates[j][0]
        for i in range(self.Configuracion.CantElite):
            candidates[i][1].Elite()
        return poblacionInicial

    def Crossover(self, poblacionInicial: Poblacion) -> Poblacion:
        nuevaPoblacion = Poblacion()
        elite = list(filter(lambda c: c.EsElite is True, poblacionInicial.Cromosomas))
        for i in elite:
            nuevaPoblacion.Cromosomas.append(i.Clone())
        while len(nuevaPoblacion.Cromosomas) < self.Configuracion.CantidadPoblacionInicial:
            cromosoma1: Cromosoma = SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas).Clone()
            cromosoma2: Cromosoma = SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas).Clone()
            corte = randint(1, 5)
            if not 0 <= random() <= self.Configuracion.ProbabilidadCrossover:
                nuevaPoblacion.Cromosomas.append(cromosoma1.Clone())
                nuevaPoblacion.Cromosomas.append(cromosoma2.Clone())
            elif corte == 1:
                c1 = Cromosoma(cromosoma1.X, cromosoma1.Y, cromosoma2.IsometricFlip[0], cromosoma2.IsometricFlip[1])
                c1.Brightness = cromosoma2.Brightness
                c1.Contrast = cromosoma2.Contrast
                c1.RangeX = cromosoma2.RangeX
                c1.RangeY = cromosoma2.RangeY
                c2 = Cromosoma(cromosoma2.X, cromosoma2.Y, cromosoma1.IsometricFlip[0], cromosoma1.IsometricFlip[1])
                c2.Brightness = cromosoma1.Brightness
                c2.Contrast = cromosoma1.Contrast
                c2.RangeX = cromosoma1.RangeX
                c2.RangeY = cromosoma1.RangeY
                nuevaPoblacion.Cromosomas.append(c1)
                nuevaPoblacion.Cromosomas.append(c2)
            elif corte == 2:
                c1 = Cromosoma(cromosoma1.X, cromosoma1.Y, cromosoma2.IsometricFlip[0], cromosoma2.IsometricFlip[1])
                c1.Brightness = cromosoma2.Brightness
                c1.Contrast = cromosoma2.Contrast
                c1.RangeX = cromosoma2.RangeX
                c1.RangeY = cromosoma2.RangeY
                c2 = Cromosoma(cromosoma2.X, cromosoma2.Y, cromosoma1.IsometricFlip[0], cromosoma1.IsometricFlip[1])
                c2.Brightness = cromosoma1.Brightness
                c2.Contrast = cromosoma1.Contrast
                c2.RangeX = cromosoma1.RangeX
                c2.RangeY = cromosoma1.RangeY
                nuevaPoblacion.Cromosomas.append(c1)
                nuevaPoblacion.Cromosomas.append(c2)
            elif corte == 3:
                c1 = Cromosoma(cromosoma1.X, cromosoma1.Y, cromosoma1.IsometricFlip[0], cromosoma2.IsometricFlip[1])
                c1.Brightness = cromosoma2.Brightness
                c1.Contrast = cromosoma2.Contrast
                c1.RangeX = cromosoma2.RangeX
                c1.RangeY = cromosoma2.RangeY
                c2 = Cromosoma(cromosoma2.X, cromosoma2.Y, cromosoma2.IsometricFlip[0], cromosoma1.IsometricFlip[1])
                c2.Brightness = cromosoma1.Brightness
                c2.Contrast = cromosoma1.Contrast
                c2.RangeX = cromosoma1.RangeX
                c2.RangeY = cromosoma1.RangeY
                nuevaPoblacion.Cromosomas.append(c1)
                nuevaPoblacion.Cromosomas.append(c2)
            elif corte == 4:
                c1 = cromosoma1.Clone()
                c1.Brightness = cromosoma2.Brightness
                c1.Contrast = cromosoma2.Contrast
                c1.RangeX = cromosoma2.RangeX
                c1.RangeY = cromosoma2.RangeY
                c2 = cromosoma2.Clone()
                c2.Brightness = cromosoma1.Brightness
                c2.Contrast = cromosoma1.Contrast
                c2.RangeX = cromosoma1.RangeX
                c2.RangeY = cromosoma1.RangeY
                nuevaPoblacion.Cromosomas.append(c1)
                nuevaPoblacion.Cromosomas.append(c2)
            elif corte == 5:
                c1 = cromosoma1.Clone()
                c1.Brightness = cromosoma1.Brightness
                c1.Contrast = cromosoma2.Contrast
                c1.RangeX = cromosoma2.RangeX
                c1.RangeY = cromosoma2.RangeY
                c2 = cromosoma2.Clone()
                c2.Brightness = cromosoma2.Brightness
                c2.Contrast = cromosoma1.Contrast
                c2.RangeX = cromosoma1.RangeX
                c2.RangeY = cromosoma1.RangeY
                nuevaPoblacion.Cromosomas.append(c1)
                nuevaPoblacion.Cromosomas.append(c2)
            elif corte == 6:
                c1 = cromosoma1.Clone()
                c1.Brightness = cromosoma1.Brightness
                c1.Contrast = cromosoma1.Contrast
                c1.RangeX = cromosoma2.RangeX
                c1.RangeY = cromosoma2.RangeY
                c2 = cromosoma2.Clone()
                c2.Brightness = cromosoma2.Brightness
                c2.Contrast = cromosoma2.Contrast
                c2.RangeX = cromosoma1.RangeX
                c2.RangeY = cromosoma1.RangeY
                nuevaPoblacion.Cromosomas.append(c1)
                nuevaPoblacion.Cromosomas.append(c2)
            elif corte == 7:
                c1 = cromosoma1.Clone()
                c1.Brightness = cromosoma1.Brightness
                c1.Contrast = cromosoma1.Contrast
                c1.RangeX = cromosoma1.RangeX
                c1.RangeY = cromosoma2.RangeY
                c2 = cromosoma2.Clone()
                c2.Brightness = cromosoma2.Brightness
                c2.Contrast = cromosoma2.Contrast
                c2.RangeX = cromosoma2.RangeX
                c2.RangeY = cromosoma1.RangeY
                nuevaPoblacion.Cromosomas.append(c1)
                nuevaPoblacion.Cromosomas.append(c2)

        return nuevaPoblacion

    def Mutacion(self, poblacionInicial: Poblacion):
        """Recorre los cromosomas no elites de una poblacion y evalua si debe aplicar mutacion"""
        cromosomasNoElites = list(filter(lambda c: c.EsElite is False, poblacionInicial.Cromosomas))
        for cromosoma in cromosomasNoElites:
            if 0 <= random() <= self.Configuracion.ProbabilidadMutacion:
                numeroParametro = randint(1, 4)
                if numeroParametro == 1:
                    cromosoma.IsometricFlip = choice(direction), cromosoma.IsometricFlip[1]
                elif numeroParametro == 2:
                    cromosoma.IsometricFlip = cromosoma.IsometricFlip[0], choice(angle)
                elif numeroParametro == 3:
                    cromosoma.Brightness = cromosoma.Brightness + random()
                elif numeroParametro == 4:
                    cromosoma.Contrast = cromosoma.Brightness + random()

