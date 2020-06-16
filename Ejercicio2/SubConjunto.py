from Ejercicio2.Object import Object


# Clase que contiene una lista de Items en este caso seran del tipo Object
class SubConjunto:
    def __init__(self, items: []):
        self.items: Object = items  # Guarda los objetos en una propiedad

    # Devuelve la suma de los volumenes de los items(o el peso en la segunda parte)
    def GetVolumen(self):
        return sum(objeto.unit for objeto in self.items)

    # Devuelve la suma de los pricios de los items
    def GetPrice(self):
        return sum(objeto.price for objeto in self.items)
