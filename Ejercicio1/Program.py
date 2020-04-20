from Ejercicio1.AlgoritmoGenetico import AlgoritmoGenetico
from Ejercicio1.Configuracion import Configuracion


class Program:
    def __init__(self):
        pass

    def Run(self):
        exit = False
        while exit == False:
            configuracion = self.IngresarConfiguracion()
            algoritmo = AlgoritmoGenetico(configuracion)
            algoritmo.Run()
            algoritmo.Print()
            algoritmo.ExportToExcel()
            line = input("Correr Nuevamente? [Y,N]")
            if (line.lower() == "n"):
                exit = True

    def IngresarConfiguracion(self) -> Configuracion:
        porcentajeCrossOver = float(input("Porcentaje Crossover (float): "))
        porcentajeMutacion = float(input("Porcentaje Mutacion (float): "))
        cantidadInicialPoblacion = int(input("Cantidad Inicial Poblacion (int): "))
        iteraciones = int(input("Cantidad Iteraciones (int): "))
        printCrossovers = input("Imprimir Crossovers (bool): ")
        printMutaciones = input("Imprimir Mutaciones (bool): ")

        printCrossoversBool = False
        if (printCrossovers == "1" or printCrossovers == "True"):
            printCrossoversBool = True
        printMutacionesBool = False
        if (printMutaciones == "1" or printMutaciones == "True"):
            printMutacionesBool = True

        return Configuracion(porcentajeCrossOver, porcentajeMutacion, cantidadInicialPoblacion, iteraciones,
                             printCrossoversBool, printMutacionesBool)
