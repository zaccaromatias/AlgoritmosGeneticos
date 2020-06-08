from Ejercicio2.Listitem import Item


class Mochila:
    def __init__(self, price, capacity):
        self.price = price
        self.capacity = capacity


mochila = Mochila(0, Item.MAXIMUMWEIGHT)

subsets = []
sumprice = 0
sumvolumen = 0


def Subsets():
    objects = len(Item.objects)
    # operaciones de bit a bit
    countsubset = int(1 << objects)
    index = 0
    global subsets

    for p in range(countsubset):
        subsets.append(p)
        subset = []
        for item in range(objects):
            tem = (p and (1 << item))
            # usando la mascara para la operacion binaria
            if (p and (1 << item)) > 0:
                subset.append(item)
                subset[item] = Item.objects[item]
            if len(subset) > 0:
                subsets[p] = subset
        countsubset -= 1
        index += 1
    return subsets


def BestSubsets(Bsb):
    mjsub = []
    best = 0
    count = 0
    global sumvolumen
    global sumprice
    for b in range(len(Bsb)):
        if b > 0:
            for m in Bsb[b]:
                if (m.volumen <= mochila.capacity):
                    val = m.volumen
                    if (val > best):
                        mjsub.append(count)
                        mjsub[count] = m
                        sumvolumen += m.volumen
                        sumprice += m.price  # Equivale a sumprice = sumprice + m.price
                        best = val
                        count += 1
    return mjsub


print("Antes de la seleccion: ")
Sub = Subsets()
Bsub = BestSubsets(Sub)

print("Maximización: ")
for i in range(len(Bsub)):
    print("Objeto ", Bsub[i].name, " Precio: ", Bsub[i].price, " Volumen: ", Bsub[i].volumen)
print()
print("Volumen total en cm3: ", sumvolumen)
print("Precio total: $", sumprice)
