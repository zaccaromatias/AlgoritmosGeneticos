class Capital:
    def __init__(self, nombre, indice):
        self.Nombre = nombre
        self.Indice = indice
        self.Visitada = False

    def __str__(self):
        return self.Nombre

    def SetVisitada(self, value: bool):
        self.Visitada = value
        return self
