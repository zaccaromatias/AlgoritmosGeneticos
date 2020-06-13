import Ejercicio2.Funtion as funct
import Ejercicio2.Datagrid as data

#Variable global
subsets = [] #variable para guarda todos los subconjunto
Bestsubset = [] #variable para guarda el mejor subconjunto
best = []


def Subsets(items,subsets):
    objects = len(items.objects)
    # operaciones de bit a bit --> te permite ver cuando subconjunto va a tener
    countsubset = int(1 << objects)
    index = 0
    for p in range(countsubset):
        subsets.append(p)
        subset = []
        index = 0
        for item in range(objects):
            """"" 
            usando la mascara para la operacion binaria.
            Permite de definir el rango entre 1 y 0.
            Nos permite de simplificar usar de funcion
            Las operaciones que sobre ella se realizan son rapidas
            Nos permite tener un menor carga  de pila.
            Nos permite de resolver el problema sin iterar  
            """""
            if (p & (1 << item)) > 0:
                subset.append(index)
                subset[index] = items.objects[item]
                index += 1
        subsets[p] = subset
    return subsets


def BestSubsets(Sub, MAXIMUMWEIGHT, Bestsubset):
    best = 0
    for b in range(len(Sub)):
        #Comparando si el volumen de esta conjunto esta dentro del limite max de la mochila
        if (funct.GetVolumen(Sub[b]) <= MAXIMUMWEIGHT):
            val = funct.GetValue(Sub[b])
            #Busquando el mejor subconjunto
            if (val > best):
                Bestsubset = Sub[b]
                best = val
    return Bestsubset

class Mochila:
    def __init__(self, Obj):
        self.Obj = Obj

    global subsets
    global Bestsubset

    def Run(self):
        Sub = Subsets( self, subsets )
        best = BestSubsets( Sub, self.MAXIMUMWEIGHT, Bestsubset )
        # Grid para mostrar el resultado final
        data.GenerarGrid(best,"Volumen cm3","Volumen total en cm3","Precio total",False)