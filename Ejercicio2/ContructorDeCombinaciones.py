from Ejercicio2.Listitem import Item


def ConstruirPosiblesCombinaciones(objetos: []) -> []:
    count = len(objetos)
    ##Esta es la magia de Eugene para sacar las posibles combinaciones
    numeroDeCombinacionesPosibles = int(1 << count)
    # Recorro ese numero de combinacionesPosibles osea de 0 a X(1024)
    combinaciones = []
    for number in range(numeroDeCombinacionesPosibles):
        # Convierte el numero en binario ejemplo para el numero 5 = '0b101' con el [2:] hago que tome solo lo que esta despues de la b
        binario = bin(number)[2:]
        binarioLista = list(binario)  # Convierte a lista el valor anterior
        # Busca los indices donde haya un 1
        indicesConValorUno = list(filter(lambda i: binarioLista[i] == '1', range(len(binarioLista))))
        # Aca se podria crear alguna clase nueva de nombre SubConjunto con una propiedad con estos items
        subConjunto = []
        for indice in indicesConValorUno:
            subConjunto.append(objetos[indice])
        combinaciones.append(subConjunto)
    return combinaciones

#Forma de usarlo
todasLasCombinaciones = ConstruirPosiblesCombinaciones(Item.objects)
print(todasLasCombinaciones)
