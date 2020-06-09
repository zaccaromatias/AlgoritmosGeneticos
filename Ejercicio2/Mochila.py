from Ejercicio2.Listitem import Item
import Ejercicio2.Funtion as funct

class Mochila:
    def __init__(self, price, capacity):
        self.price = price
        self.capacity = capacity

mochila = Mochila(0, Item.MAXIMUMWEIGHT)

subsets = []
mjsub = []
sumprice = 0
sumvolumen = 0


def Subsets():
    objects = len(Item.objects)
    # operaciones de bit a bit
    countsubset = int(1 << objects)
    global subsets
    index = 0
    for p in range(countsubset):
        subsets.append(p)
        subset = []
        index = 0
        for item in range(objects):
            # usando la mascara para la operacion binaria
            if (p & (1 << item)) > 0:
                subset.append(index)
                subset[index] = Item.objects[item]
                index += 1
        subsets[p] = subset
    return subsets


def BestSubsets(Bsb):
    global subsets
    best = 0
    count = 0
    global sumvolumen
    global sumprice
    global mjsub
    for b in range(len(Bsb)):
        if (funct.GetVolumen(Bsb[b]) <= mochila.capacity):
            val = funct.GetValue(Bsb[b])
            if (val > best):
                mjsub.append(0)
                mjsub = Bsb[b]
                best = val
                count += 1
    return mjsub


print("Antes de la seleccion: ")
Sub = Subsets()
BestSubsets(Sub)

print("Maximización: ")
for i in range(len(mjsub)):
    print("Objeto ", mjsub[i].name, " Precio: ", mjsub[i].price, " Volumen: ", mjsub[i].volumen)
    sumvolumen += mjsub[i].volumen
    sumprice += mjsub[i].price  # Equivale a sumprice = sumprice + m.price
print()
print("Volumen total en cm3: ", sumvolumen)
print("Precio total: $", sumprice)
