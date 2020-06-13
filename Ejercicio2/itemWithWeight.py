from Ejercicio2.Object import Object

class Item:
    pass

# Item: "Nombre del paquete", Precio, Volumen
class Itemweight:
    objects = []
    objects.append(Object(1, 72, 1800))
    objects.append(Object(2, 36, 600))
    objects.append(Object(3, 60, 1200))

    MAXIMUMWEIGHT = 3000