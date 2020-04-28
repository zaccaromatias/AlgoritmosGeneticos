from Ejercicio1.AlgoritmoGenetico import AlgoritmoGenetico
from Ejercicio1.Configuracion import Configuracion


def IngresarConfiguracion() -> Configuracion:
    porcentajeCrossOver = 0.75                  # float(input("Porcentaje Crossover (float): "))
    porcentajeMutacion = 0.05                   # float(input("Porcentaje Mutacion (float): "))
    cantidadInicialPoblacion = 10               # int(input("Cantidad Inicial Poblacion (int): "))
    iteraciones = int(input("Cantidad Iteraciones (int): "))
    eliteBool = input("Elitismo (1-Sí/otro-No): ")
    if eliteBool == "1":
        elite = True
    else:
        elite = False
    # printCrossovers = input("Imprimir Crossovers (bool): ")
    # printMutaciones = input("Imprimir Mutaciones (bool): ")

    # printCrossoversBool = False
    # if printCrossovers == "1" or printCrossovers == "True":
    #     printCrossoversBool = True
    # printMutacionesBool = False
    # if printMutaciones == "1" or printMutaciones == "True":
    #     printMutacionesBool = True

    return Configuracion(porcentajeCrossOver, porcentajeMutacion, cantidadInicialPoblacion, iteraciones,
                         elite)


class Program:
    def __init__(self):
        pass

    def Run(self):
        exit = False
        while not exit:
            configuracion = IngresarConfiguracion()
            algoritmo = AlgoritmoGenetico(configuracion)
            algoritmo.Run()
            algoritmo.Print()
            algoritmo.ExportToExcel()
            # line = input("Correr Nuevamente? [Y,N]: ")
            # if line.lower() == "n":
            exit = True