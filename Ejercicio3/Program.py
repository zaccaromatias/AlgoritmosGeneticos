# Clase que solicita la entrada de los parámetros de entrada de configuración
# para crear una instancia de la clase AlgoritmoGenetico
# para ejecutar los siguientes métodos del mismo Run(), Print() y ExportToExcel()
# Mas logica para ejecutar de nuevo el programa

from Ejercicio3.AlgoritmoGenetico import AlgoritmoGenetico
from Ejercicio3.Configuracion import Configuracion
from Ejercicio3.DistanciaHelper import DistanciaHelper
from Ejercicio3.Heuristica import Heuristica
from Ejercicio3.MapHelper import MapHelper


def IngresarConfiguracion() -> Configuracion:
    """Ingreso de parámetros para el AG"""
    """porcentajeCrossOver = float(input("Porcentaje Crossover (float): "))
    porcentajeMutacion = float(input("Porcentaje Mutacion (float): "))
    cantidadInicialPoblacion = int(input("Ciudad Inicial (int o null): "))
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
        elite = False"""

    # CÓDIGO PARA PRUEBA DE SISTEMA
    # printCrossovers = input("Imprimir Crossovers (bool): ")
    # printMutaciones = input("Imprimir Mutaciones (bool): ")
    # printCrossoversBool = False
    # if printCrossovers == "1" or printCrossovers == "True":
    #     printCrossoversBool = True
    # printMutacionesBool = False
    # if printMutaciones == "1" or printMutaciones == "True":
    #     printMutacionesBool = True
    return Configuracion(0.75, 0.05, 50, 20,
                         False, False, 2)
    """return Configuracion(porcentajeCrossOver, porcentajeMutacion, cantidadInicialPoblacion, iteraciones,
                         elite, diversidadGenetica)"""


def Initial():
    """Muestra menú de opciones"""
    print("Elegir el punto que desea ejecutar:\n"
          "1 - Heurística Desde Determinada Ciudad\n"
          "2 - Heurística Óptimo\n"
          "3 - Algoritmo Genético\n"
          "4 - AG con Elitismo\n"
          "5 - Salir\n")


class Program:
    def __init__(self):
        pass

    @staticmethod
    def Run():
        """Ejecuta programa principal"""
        opt = 0
        while opt != 5:
            print()
            Initial()
            opt = input("Ingrese opción: ")
            if opt == "1":
                ciudadElegida = int(input("Ciudad de partida: "))
                recorrido = Heuristica.CalcularRecorridoIniciandoEn(DistanciaHelper.Capitales[ciudadElegida])
                DistanciaHelper.PrintRecorrido(recorrido)
                MapHelper.DibujarMapa(recorrido)
            elif opt == "2":
                recorrido = Heuristica.CalcularMejorRecorrido()
                DistanciaHelper.PrintRecorrido(recorrido)
                MapHelper.DibujarMapa(recorrido)
            elif opt == "3":
                configuracion = IngresarConfiguracion()
                algoritmo = AlgoritmoGenetico(configuracion)
                algoritmo.Run()
                mejor = algoritmo.GetMejorCromosomaDeTodasLasPoblaciones()
                DistanciaHelper.PrintRecorrido(mejor[1].GetAllCiudades())
                MapHelper.DibujarMapa(mejor[1].GetAllCiudades())
                """algoritmo.ExportToExcel()"""
            elif opt == "5":
                break
            input("Presione Enter para continuar...")
