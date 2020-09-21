class Capital:
    def __init__(self, nombre, indice, lat, long):
        self.Nombre = nombre
        self.Indice = indice
        self.Visitada = False
        self.Lat = lat
        self.Long = long

    def __str__(self):
        return self.Nombre

    def SetVisitada(self, value: bool):
        self.Visitada = value
        return self
