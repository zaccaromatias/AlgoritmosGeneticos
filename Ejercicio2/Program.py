from Ejercicio2.Mochila import Mochila
from Ejercicio2.Items import Items


def Initial():
    print("Elegir el punto que desea ejecutar:\n "
          "1 - Búsqueda exhaustiva con volumen ----> Marque 1\n"
          " 2 - Algoritmo Greedy con volumenen ----> Marque 2 \n"
          " 3 - Búsqueda exhaustiva con gramos ----> Marque 3\n"
          " 4 - Algoritmo Greedy con gramos ----> Marque 4 \n"
          " 5 - Si desea salir ----> Marque 5 \n")


class Program:
    def __init__(self):
        pass

    def Run(self):
        VALOR_MAXIMO_VOLUMEN_MOCHILA = 4200
        VALOR_MAXIMO_PESO_MOCHILA = 3000
        Initial()
        val = input("Ingrese Opcion : ")
        while True:
            if val == "1":
                mochila = Mochila(Items.ObjetosParaMochilaPorVolumen, VALOR_MAXIMO_VOLUMEN_MOCHILA, "Volumen", "Cm3")
                mochila.BusquedaExhaustiva()
            elif val == "2":
                mochila = Mochila(Items.ObjetosParaMochilaPorVolumen, VALOR_MAXIMO_VOLUMEN_MOCHILA, "Volumen", "Cm3")
                mochila.BusquedaGredy()
            elif val == "3":
                mochila = Mochila(Items.ObjetosParaMochilaPorPeso, VALOR_MAXIMO_PESO_MOCHILA, "Peso", "g")
                mochila.BusquedaExhaustiva()
            elif val == "4":
                mochila = Mochila(Items.ObjetosParaMochilaPorPeso, VALOR_MAXIMO_PESO_MOCHILA, "Peso", "g")
                mochila.BusquedaGredy()
            elif val == "5":
                return
            input("Precione enter para continuar")
            Initial()
            val = input("Ingrese Opcion : ")
