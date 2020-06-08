class Object:
    def __init__(self, name, price, volumen):
        self.name = name
        self.price = price
        self.volumen = volumen
        self.volumenPerUnit = self.volumen / self.price
