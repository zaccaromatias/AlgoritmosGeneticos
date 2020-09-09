# Clase que solicita la entrada de los parámetros de entrada de configuración
# para crear una instancia de la clase AlgoritmoGenetico
# para ejecutar los siguientes métodos del mismo Run(), Print() y ExportToExcel()
# Mas logica para ejecutar de nuevo el programa
from Ejercicio3.AlgoritmoGenetico import AlgoritmoGenetico
from Ejercicio3.Configuracion import Configuracion
from Ejercicio3.DistanciaHelper import DistanciaHelper
from Ejercicio3.Heuristica import Heuristica

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

def Initial():
    print("Elegir el punto que desea ejecutar:\n "
          "1 - Heurística Desde Determinada Ciudad ----> Marque 1\n"
          " 2 - Heurística Óptimo ----> Marque 2 \n"
          " 3 - Algoritmo Genético ----> Marque 3\n"
          " 4 - Si desea salir ----> Marque 5 \n")

class Program:
    def __init__(self):
        pass

    def Run(self):
        exit = False
        DistanciaHelper.LoadTablaDistanicaYCapitales()
        cuidad = DistanciaHelper.Capitales
        DistanciaHelper.GetAllCuidad(cuidad)
        DistanciaHelper.InicialCuidadVisitado(cuidad)
        print()
        Initial()
        val = input("Ingrese Opcion : ")
        while True:
            """configuracion = IngresarConfiguracion()
            algoritmo = AlgoritmoGenetico(configuracion)
            algoritmo.Run()
            algoritmo.Print()
            algoritmo.ExportToExcel()
            line = "n"  # input("Correr Nuevamente? [Y,N]: ")
            if line.lower() == "n":
                exit = True"""
            if val == "1":
                cuidadElegida = int(input("Cuidad de partida : "))
                Heuristica.GetRecorrerCuidad(cuidadElegida, cuidad)
                Heuristica.PrintRecorrido()

            input("Precione enter para continuar")
            Initial()
            val = input("Ingrese Opcion : ")
