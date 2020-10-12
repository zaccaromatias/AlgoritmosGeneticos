from TP_Investigacion_Fractales.ImagenHelper import *
from TP_Investigacion_Fractales.PorcionRuleta import PorcionRuleta
from random import randint

from TP_Investigacion_Fractales.Transformacion import Transformacion


class Cromosoma:
    def __init__(self):
        self.EsElite = False
        self.PorcionRuleta = PorcionRuleta()
        self.Transformaciones = []

    def CargarTransformacionesAleatorias(self, transformed_blocks, i_count, j_count, img, destination_size):
        for i in range(i_count):
            self.Transformaciones.append([])
            for j in range(j_count):
                self.Transformaciones[i].append(None)
                D = img[i * destination_size:(i + 1) * destination_size,
                    j * destination_size:(j + 1) * destination_size]
                indice = randint(0, len(transformed_blocks) - 1)
                k, l, direction, angle, S = transformed_blocks[indice]
                contrast, brightness = find_contrast_and_brightness2(D, S)
                self.Transformaciones[i][j] = Transformacion(i, j, k, l, direction, angle, contrast, brightness, D, S)
        self.RefreshValorObjetivo()
        return self

    def Reset(self):
        self.PorcionRuleta = PorcionRuleta()
        self.EsElite = False

    def RefreshValorObjetivo(self):
        sum = 0
        for transformacionI in self.Transformaciones:
            for transformacion in transformacionI:
                sum += transformacion.GetDistancia()
        self.ValorObjetivo = sum

    def FuncionObjetivo(self, img, source_size, destination_size, step):
        return self.ValorObjetivo

    # Marca cromosoma que es elite
    def Elite(self):
        self.EsElite = True

    # cambia valor del cromosoma
    def Mutar(self, img, step, source_size, factor):
        indice = randint(0, len(self.Transformaciones) - 1)
        indice2 = randint(0, len(self.Transformaciones[indice]) - 1)
        self.Transformaciones[indice][indice2].Mutar(img, step, source_size, factor)
        self.RefreshValorObjetivo()

        # Devuelve una instancia nueva pero con mismos valores
        # Para evitar valores por referencia

    def Clone(self):
        cromosoma = Cromosoma()
        cromosoma.EsElite = self.EsElite
        cromosoma.Transformaciones = self.Transformaciones
        cromosoma.ValorObjetivo = self.ValorObjetivo
        return cromosoma
