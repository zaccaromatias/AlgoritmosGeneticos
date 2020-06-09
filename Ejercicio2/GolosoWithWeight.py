from Ejercicio2.itemWithWeight import Item

class MochilaWithWeightGreevy:
    def __init__(self, price, capacity):
        self.price = price
        self.capacity = capacity

    def PutObject(self, object):
        self.price += object.price


mochila = MochilaWithWeightGreevy(0, Item.MAXIMUMWEIGHT)


# algoritmo de ordenación por selección
def SelectionSort(list, tam):
    for i in range(0, tam - 1):
        min = i
        for j in range(i + 1, tam):
            if list[min].volumenPerUnit > list[j].volumenPerUnit:
                min = j
        aux = list[min]
        list[min] = list[i]
        list[i] = aux


resultado = []
sumprice = 0
sumweight = 0

voltotal = 0
count = 0

for i in range(len(Item.objects)):
    object = Item.objects[i]
    if (voltotal + object.weight) <= mochila.capacity:
        resultado.append(count)
        resultado[count] = object
        mochila.PutObject(object)
        voltotal += object.weight
        sumweight += object.weight
        sumprice += object.price
        count += 1

print("Resultado: Fracciones de los objetos en la mochila: ")
for i in range(len(resultado)):
    print("Objeto ", resultado[i].name, " Precio: ", resultado[i].price, " Volumen: ", resultado[i].weight,
          " Porcion por unidad o Ratio: ", resultado[i].weightPerUnit)
print()
print("Volumen total en cm3: ", sumweight)
print("Precio total: $", sumprice)