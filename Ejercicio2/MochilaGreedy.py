from Ejercicio2.Listitem import Item

class MochilaGreevy:
    def __init__(self, price, capacity):
        self.price = price
        self.capacity = capacity

    def PutObject(self, object):
        self.price += object.price


mochila = MochilaGreevy(0, Item.MAXIMUMWEIGHT)


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
sumvolumen = 0

voltotal = 0
count = 0
SelectionSort(Item.objects, len(Item.objects))

for i in range(len(Item.objects)):
    object = Item.objects[i]
    if (voltotal + object.volumen) <= mochila.capacity:
        resultado.append(count)
        resultado[count] = object
        mochila.PutObject(object)
        voltotal += object.volumen
        sumvolumen += object.volumen
        sumprice += object.price
        count += 1

print("Resultado: Fracciones de los objetos en la mochila: ")
for i in range(len(resultado)):
    print("Objeto ", resultado[i].name, " Precio: ", resultado[i].price, " Volumen: ", resultado[i].volumen,
          " Porcion por unidad o Ratio: ", resultado[i].volumenPerUnit)
print()
print("Volumen total en cm3: ", sumvolumen)
print("Precio total: $", sumprice)
