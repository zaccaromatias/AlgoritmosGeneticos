# Clase que solicita la entrada de los parámetros de entrada de configuración
# para crear una instancia de la clase AlgoritmoGenetico
# para ejecutar los siguientes métodos del mismo Run(), Print() y ExportToExcel()
# Mas logica para ejecutar de nuevo el programa
from Ejercicio3.AlgoritmoGenetico import AlgoritmoGenetico
from Ejercicio3.Configuracion import Configuracion
from Ejercicio3.DistanciaHelper import DistanciaHelper

def IngresarConfiguracion() -> Configuracion:
    porcentajeCrossOver = float(input("Porcentaje Crossover (float): "))
    porcentajeMutacion = float(input("Porcentaje Mutacion (float): "))
    cantidadInicialPoblacion = int(input("Cantidad Inicial Poblacion (int): "))
    iteraciones = int(input("Cantidad Iteraciones (int): "))
    diversidadBool = input("Diversidad genética? (1-Sí/otro-No): ")
    if diversidadBool == "1":
        diversidadGenetica = True
    else:
        diversidadGenetica = False
    eliteBool = input("Elitismo? (1-Sí/otro-No): ")
    if eliteBool == "1":
        elite = True
    else:
        elite = False

    # CÓDIGO PARA PRUEBA DE SISTEMA
    # printCrossovers = input("Imprimir Crossovers (bool): ")
    # printMutaciones = input("Imprimir Mutaciones (bool): ")
    # printCrossoversBool = False
    # if printCrossovers == "1" or printCrossovers == "True":
    #     printCrossoversBool = True
    # printMutacionesBool = False
    # if printMutaciones == "1" or printMutaciones == "True":
    #     printMutacionesBool = True

    return Configuracion(porcentajeCrossOver, porcentajeMutacion, cantidadInicialPoblacion, iteraciones,
                         elite, diversidadGenetica)


class Program:
    def __init__(self):
        pass

    def Run(self):
        exit = False
        DistanciaHelper.LoadTablaDistanicaYCapitales()
        while not exit:
            configuracion = IngresarConfiguracion()
            algoritmo = AlgoritmoGenetico(configuracion)
            algoritmo.Run()
            algoritmo.Print()
            algoritmo.ExportToExcel()
            line = "n"  # input("Correr Nuevamente? [Y,N]: ")
            if line.lower() == "n":
                exit = True
