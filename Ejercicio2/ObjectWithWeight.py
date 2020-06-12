class ObjectWithWeight:
    def __init__(self, name, price, unit):
        self.name = name
        self.price = price
        self.unit = unit
        self.Ratio = self.unit / self.price