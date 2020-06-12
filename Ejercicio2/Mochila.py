from Ejercicio2.Listitem import Item
import Ejercicio2.Funtion as funct
import Ejercicio2.Datagrid as data

#Variable global
subsets = [] #variable para guarda todos los subconjunto
Bestsubset = [] #variable para guarda el mejor subconjunto
sumprice = 0
sumvolumen = 0
best = []


def Subsets(items,subsets):
    objects = len(items)
    # operaciones de bit a bit --> te permite ver cuando subconjunto va a tener
    countsubset = int(1 << objects)
    index = 0
    for p in range(countsubset):
        subsets.append(p)
        subset = []
        index = 0
        for item in range(objects):
            # usando la mascara para la operacion binaria
            if (p & (1 << item)) > 0:
                subset.append(index)
                subset[index] = items[item]
                index += 1
        subsets[p] = subset
    return subsets


def BestSubsets(Bsb,Bestsubset):
    best = 0
    for b in range(len(Bsb)):
        if (funct.GetVolumen(Bsb[b]) <= Item.MAXIMUMWEIGHT):
            val = funct.GetValue(Bsb[b])
            if (val > best):
                Bestsubset = Bsb[b]
                best = val
    return Bestsubset


class Mochila:
    def __init__(self, Obj):
        self.Obj = Obj

    global subsets
    global Bestsubset

    def Run(self):
        Sub = Subsets( self, subsets )
        best = BestSubsets( Sub, Bestsubset )
        global sumvolumen
        global sumprice
        data.GenerarGrid(best,"Volumen cm3","Volumen total en cm3","Precio total",False)

        """for i in range( len( best ) ):
            print( "Objeto ", best[i].name, " Precio: ", best[i].price, " Volumen: ", best[i].volumen )
            sumvolumen += best[i].volumen
            sumprice += best[i].price  # Equivale a sumprice = sumprice + m.price
        print()
        print( "Volumen total en cm3: ", sumvolumen )
        print( "Precio total: $", sumprice )"""