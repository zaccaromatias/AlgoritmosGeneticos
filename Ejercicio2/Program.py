from Ejercicio2.Mochila import Mochila
from Ejercicio2.MochilaGreedy import MochilaGreevy
from Ejercicio2.GolosoWithWeight import MochilaWithWeightGreevy
from Ejercicio2.Listitem import Item
def Initial():
    print( "Elegir el punto que desea ejecutar:\n "
           "1- Búsqueda exhaustiva con volum ----> Marque A\n"
           " 2- Algoritmo Greedy con volumen----> Marque B \n"
           " 3- Búsqueda exhaustiva con gramo ----> Marque C\n"
           " 4- Algoritmo Greedy con gramo----> Marque D \n"
           " 5- Si desea salir----> Marque E \n")

class Program:
    def __init__(self):
        pass


    def Run(self):

        sumprice = 0
        sumvolumen = 0
        exit = False
        while not exit:
            Initial()
            val = input( "Ingrese la letra elegida : " )
            if val.lower() == "a":
                val = Mochila.Run(Item.objects)
            elif val.lower() == "b":
                val = MochilaGreevy.Run()
            elif val.lower() == "c":
                val = Mochila.Run()
            elif val.lower() == "d":
                val = MochilaWithWeightGreevy.Run()
            elif val.lower() == "s":
                exit = True
            exit = True