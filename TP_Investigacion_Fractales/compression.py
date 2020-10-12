import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math
from TP_Investigacion_Fractales.AlgoritmoGenetico import AlgoritmoGenetico
from TP_Investigacion_Fractales.Configuracion import Configuracion








# ----------------------------------------------------------------------------------------------------------------------
#                                                       Main
# ----------------------------------------------------------------------------------------------------------------------



if __name__ == '__main__':
    whileCond = True
    while whileCond:
        Input = '3'  # input("1- Heurística GS\n"
        #  "2- Heurística RGB\n"
        #  "3- AG\n"
        #  "Opción: ")
        if Input == '1':
            test_greyscale()
        elif Input == '2':
            test_rgb()
        elif Input == '3':
            test_ga()
        else:
            print("Opción inválida. Intente otra vez.")
            continue
        whileCond = False
