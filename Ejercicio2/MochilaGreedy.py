from Listitem import Item
class MochilaGreevy:
    def __init__(self, weight, capacity):
        self.weight = weight
        self.capacity = capacity

    def PutObject(self, object):
        self.weight += object.weight

mochila = MochilaGreevy(0, Item.MAXIMUMWEIGHT)
# algoritmo de ordenación por selección
def SelectionSort( list, tam):
    for i in range(0, tam - 1):
        min = i
        for j in range(i + 1, tam):
            if list[min].weight > list[j].weight:
                min = j
        aux = list[min]
        list[min] = list[i]
        list[i] = aux


resultado = []
sumweight = 0
sumval = 0

voltotal = 0
count = 0
for i in range(len(Item.objects) - 1):
    object = Item.objects[i]
    if (voltotal + object.value) <= mochila.capacity:
        resultado.append(count)
        resultado[count] = object
        mochila.PutObject(object)
        voltotal += object.value
        sumval = sumval + object.value
        sumweight = sumweight + object.weight
        count += 1


print("Resultado: Fracciones de los objetos en la mochila: ")
for i in range(len(resultado) - 1, -1, -1):
    print("Objeto ", i, " Peso: ", resultado[i].weight," Volumen: ", resultado[i].value," Porcion por unidad o Ratio: ", resultado[i].ValuePerUnit)
print()
print("Volumen total en cm3: ", sumval)
print("Peso total: $", sumweight )