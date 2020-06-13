from Ejercicio2.Mochila import Mochila
from Ejercicio2.MochilaGreedy import MochilaGreevy
from Ejercicio2.Listitem import Item
from Ejercicio2.itemWithWeight import Itemweight

def Initial():
    print( "Elegir el punto que desea ejecutar:\n "
           "1- Búsqueda exhaustiva con volum ----> Marque A\n"
           " 2- Algoritmo Greedy con volumen----> Marque B \n"
           " 3- Búsqueda exhaustiva con gramo ----> Marque C\n"
           " 4- Algoritmo Greedy con gramo----> Marque D \n"
           " 5- Si desea salir----> Marque S \n")

class Program:
    def __init__(self):
        pass

    def Run(self):
        exit = False
        while not exit:
            Initial()
            val = input( "Ingrese la letra elegida : " )
            if val.lower() == "a":
                Mochila.Run(Item)
            elif val.lower() == "b":
                MochilaGreevy.Run(Item)
            elif val.lower() == "c":
                Mochila.Run(Itemweight)
            elif val.lower() == "d":
                Mochila.Run(Itemweight)
            elif val.lower() == "s":
                exit = True
            exit = True