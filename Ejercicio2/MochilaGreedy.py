from Ejercicio2.Listitem import Item
import Ejercicio2.Datagrid as data

# algoritmo de ordenación por selección
def SelectionSort(list, tam):
    for i in range(0, tam - 1):
        min = i
        for j in range(i + 1, tam):
            if list[min].Ratio > list[j].Ratio:
                min = j
        aux = list[min]
        list[min] = list[i]
        list[i] = aux
    return list

resultado = []
sumprice = 0
sumvolumen = 0
voltotal = 0
count = 0

def best(items):
    global  voltotal
    global  sumprice
    global sumvolumen
    global count
    for i in range(len(items)):
        object = items[i]
        if (voltotal + object.unit) <= Item.MAXIMUMWEIGHT:
            resultado.append(count)
            resultado[count] = object
            voltotal += object.unit
            sumvolumen += object.unit
            sumprice += object.price
            count += 1

class MochilaGreevy:
    def __init__(self, Obj):
        self.Obj = Obj

    def Run(self):
        select = SelectionSort(self, len(self))
        best(select)
        data.GenerarGrid(resultado, "Volumen cm3", "Volumen total en cm3", "Precio total",True)
        """print("Resultado: Fracciones de los objetos en la mochila: ")
        for i in range(len(resultado)):
            print("Objeto ", resultado[i].name, " Precio: ", resultado[i].price, " Volumen: ", resultado[i].volumen,
                  " Porcion por unidad o Ratio: ", resultado[i].volumenPerUnit)
        print()
        print("Volumen total en cm3: ", sumvolumen)
        print("Precio total: $", sumprice)"""
