import Ejercicio2.Datagrid as data

# algoritmo de ordenación por selección
def SelectionSort(list, tam):
    for i in range(0, tam - 1):
        min = i
        for j in range(i + 1, tam):
            if list.objects[min].Ratio > list.objects[j].Ratio:
                min = j
        aux = list.objects[min]
        list.objects[min] = list.objects[i]
        list.objects[i] = aux
    return list.objects

resultado = []
voltotal = 0
count = 0

def best(items,MAXIMUMWEIGHT):
    global  voltotal
    global count
    #empezar desde el final por que esta ordenado de menor a mayor
    for i in range(len(items)):
        object = items[i]
        if (voltotal + object.unit) <= MAXIMUMWEIGHT:
            resultado.append(count)
            resultado[count] = object
            voltotal += object.unit
            count += 1

class MochilaGreevy:
    def __init__(self, Obj):
        self.Obj = Obj

    def Run(self):
        select = SelectionSort(self, len(self.objects))
        best(select, self.MAXIMUMWEIGHT)
        #Grid para mostrar el resultado final
        data.GenerarGrid(resultado, "Volumen cm3", "Volumen total en cm3", "Precio total",True)
