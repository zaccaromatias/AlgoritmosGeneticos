from Ejercicio2.Object import Object


class SubConjunto:
    def __init__(self, items: []):
        self.items: Object = items

    def GetVolumen(self):
        return sum(objeto.unit for objeto in self.items)

    def GetPrice(self):
        return sum(objeto.price for objeto in self.items)
