from Ejercicio2.SubConjunto import SubConjunto


class Mochila:
    # La capacidad maxima de la mochila

    def __init__(self, objetos, maximum, nombrePropiedad, unidad):
        self.Objetos = objetos
        self.Combinaciones = []  # variable para guarda todos los subconjunto
        self.MejorCombinacion: SubConjunto = None  # variable para guarda el mejor subconjunto
        self.Maximum = maximum
        self.NombrePropiedad = nombrePropiedad
        self.Unidad = unidad

    def GenerarCombinaciones(self):
        cantidad = len(self.Objetos)
        self.Combinaciones = []  # Reset combinaciones
        # operaciones de bit a bit --> te permite ver cuantos subconjuntos va a tener, es decir cantidad total de combinaciones
        totalCombinaciones = int(1 << cantidad)
        index = 0
        for p in range(totalCombinaciones):
            subset = []
            index = 0
            for item in range(cantidad):
                """"" 
                Usa lo que se llama mascara para operaciones binarias.
                Permite de definir en que indices hay un 1                
                Las operaciones que sobre ella se realizan son rapidas
                Nos permite tener un menor carga  de pila.
                Nos permite resolver el problema sin iterar demaciadas veces  
                """""
                if (p & (1 << item)) > 0:
                    subset.append(index)
                    subset[index] = self.Objetos[item]
                    index += 1
            subconjunto = SubConjunto(subset)
            self.Combinaciones.append(subconjunto)

    def SetMejorCombinacion(self):
        bestPrice = 0
        # Itera todas las combinaciones
        for indice in range(len(self.Combinaciones)):
            # Compara si el volumen del subconjuto esta dentro del limite maximo de la mochila
            if (self.Combinaciones[indice].GetVolumen() <= self.Maximum):
                price = self.Combinaciones[indice].GetPrice()
                # Busquando el mejor subconjunto
                if (price > bestPrice):
                    self.MejorCombinacion = self.Combinaciones[indice]
                    bestPrice = price

    def PrintMejorCombinacion(self):
        print("Mejor Combinacion - ", self.NombrePropiedad, " Total(", self.Unidad, "): ",
              self.MejorCombinacion.GetVolumen(), " - Precio: $",
              self.MejorCombinacion.GetPrice())
        print("Objetos:")
        for object in self.MejorCombinacion.items:
            print("Objeto: ", object.name, " - ", self.NombrePropiedad, "(", self.Unidad, "): ", object.unit,
                  " - Precio ($): ", object.price)

        # Grid para mostrar el resultado final
        # data.GenerarGrid(self.MejorCombinacion.GetPrice(), "Volumen cm3", "Volumen total en cm3", "Precio total", False)

    def BusquedaExhaustiva(self):
        self.GenerarCombinaciones()
        self.SetMejorCombinacion()
        self.PrintMejorCombinacion()

    def SetMejorCombinacionPorGreedy(self):
        subConjunto = SubConjunto([])
        self.Objetos.sort(key=lambda x: x.Ratio, reverse=False)
        for i in range(len(self.Objetos)):
            object = self.Objetos[i]
            if (subConjunto.GetVolumen() + object.unit) <= self.Maximum:
                subConjunto.items.append(object)
            else:
                continue
        self.MejorCombinacion = subConjunto

    def BusquedaGredy(self):
        self.SetMejorCombinacionPorGreedy()
        self.PrintMejorCombinacion()
