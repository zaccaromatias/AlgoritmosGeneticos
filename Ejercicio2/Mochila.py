from Listitem import Item

class Mochila:
    def __init__(self, weight, capacity):
        self.weight = weight
        self.capacity = capacity

mochila = Mochila(0, Item.MAXIMUMWEIGHT)

subsets = []
sumweight = 0
sumval = 0

def Subsets():
    obj = len(Item.objects)
    #operaciones de bit a bit
    countsubset = int(1 << obj)
    index = 0
    global subsets

    for p in range(countsubset):
        subsets.append(p)
        subset = []
        for item in range(obj):
            tem = (p and (1 << item))
            #usando la mascara para la operacion binaria
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
    global sumval
    global sumweight
    for b in range(len(Bsb)):
        if b > 0:
            for m in Bsb[b]:
                if (m.value <= mochila.capacity):
                    val = m.value
                    if (val > best):
                        mjsub.append(count)
                        mjsub[count] = m
                        sumval = sumval + m.value
                        sumweight = sumweight + m.weight
                        best = val
                        count += 1
    return mjsub

print("Antes de la seleccion: ")
Sub = Subsets()
Bsub = BestSubsets(Sub)

print("Maximización: ")
for i in range(len(Bsub)):
    print("Objeto ", i, " Peso: ", Bsub[i].weight, " Volumen: ", Bsub[i].value)
print()
print("Volumen total en cm3: ", sumval)
print("Peso total: $", sumweight )
