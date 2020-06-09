class ObjectWithWeight:
    def __init__(self, name, price, weight):
        self.name = name
        self.price = price
        self.weight = weight
        self.weightPerUnit = self.weight / self.price