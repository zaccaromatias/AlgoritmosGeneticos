from Ejercicio2.SubConjunto import SubConjunto


class Mochila:

    def __init__(self, objetos, maximum, nombrePropiedad, unidad):
        self.Objetos = objetos  # Contiene todos los objetos
        self.Combinaciones = []  # variable de tipo lista que guarda todos los subconjuntos
        self.MejorCombinacion: SubConjunto = None  # variable del tipo SubConjunto que usamos para setear el mejor
        self.Maximum = maximum  # Valor maximo de la mochila para el primer caso es el volumen, para el segundo es el peso
        self.NombrePropiedad = nombrePropiedad  # Variable string que usamos para mostrar si es Peso o Volumen
        self.Unidad = unidad  # Variable string que usamos para mostrar si es Cm3 o g

    def GenerarCombinaciones(self):
        cantidad = len(self.Objetos)
        self.Combinaciones = []  # Reset combinaciones
        # operaciones de bit a bit --> te permite ver cuantos subconjuntos va a tener, es decir cantidad total de combinaciones (1024)
        # Equivalente a 2 a la 10
        totalCombinaciones = int(1 << cantidad)
        # Recorro ese numero de combinacionesPosibles (1024)
        for number in range(totalCombinaciones):
            # Convierte el numero en binario
            # Ejemplo para el numero 5 = "0b101" con el [2:] hacemos que tome solo lo que esta despues de la b
            # Siguiendo el ejemplo nos queda "101"
            binario = bin(number)[2:]
            # Busca los indices donde haya un 1
            indicesConValorUno = list(filter(lambda i: binario[i] == '1', range(len(binario))))
            # Buscamos la correspondencia de esos indices con nuestros objetos y los agrega a una lista de items
            items = []
            for indice in indicesConValorUno:
                items.append(self.Objetos[indice])
            # Instancia una clase SubConjunto con esa lista de items.
            # La clase SubConjunto contiene ademas metodos propios para sacar el volumen o preciode esos items
            subConjunto = SubConjunto(items)
            # Agregamos el subconjunto a la lista de combinaciones
            self.Combinaciones.append(subConjunto)

    def SetMejorCombinacion(self):
        # Inicializamos el mejor precio en 0
        bestPrice = 0
        # Itera todas las combinaciones
        for indice in range(len(self.Combinaciones)):
            # Compara si el volumen del subconjuto esta dentro del limite maximo de la mochila
            if (self.Combinaciones[indice].GetVolumen() <= self.Maximum):
                price = self.Combinaciones[indice].GetPrice()
                # En caso de estar Comparamos el precio del subconjunto con con el mejor hasta el momento
                # En caso de ser mejor sustituimos el precio y el subconjuto guardado en MejorCombinacion
                if (price > bestPrice):
                    self.MejorCombinacion = self.Combinaciones[indice]
                    bestPrice = price

    def PrintMejorCombinacion(self):
        # Imprime en consola los valores del mejor subconjuto obtenido
        print("Mejor Combinacion - ", self.NombrePropiedad, " Total(", self.Unidad, "): ",
              self.MejorCombinacion.GetVolumen(), " - Precio: $",
              self.MejorCombinacion.GetPrice())
        print("Objetos:")
        # Imprime los valores de los objetos del mejor subconjuto
        for object in self.MejorCombinacion.items:
            print("Objeto: ", object.name, " - ", self.NombrePropiedad, "(", self.Unidad, "): ", object.unit,
                  " - Precio ($): ", object.price)

    def BusquedaExhaustiva(self):
        # Genera las combinaciones
        self.GenerarCombinaciones()
        # Busca y setea el mejor subConjunto
        self.SetMejorCombinacion()
        # Imprime
        self.PrintMejorCombinacion()

    def SetMejorCombinacionPorGreedy(self):
        # Intanciamos una clase SubConjunto donde le pasamos [] es decir una lista vacia
        subConjunto = SubConjunto([])
        # Ordena de menor a mayor los objetos segun el Ratio (volumen/precio)
        self.Objetos.sort(key=lambda x: x.Ratio, reverse=False)
        # Recorremos los objetos y agregamos si nos da el limite de la mochila
        for i in range(len(self.Objetos)):
            object = self.Objetos[i]
            # subConjunto.GetVolumen() devuelve la suma de los objetos hasat el momento en el subconjunto
            # suma lo del objeto que esta iterando
            # y verifica si supera el valor maximo que se establecio al instanciar la mochila
            # En caso de que no lo supere lo agrega al subconjunto sino sigue con el proximo
            if (subConjunto.GetVolumen() + object.unit) <= self.Maximum:
                subConjunto.items.append(object)
        # Setea ese subconjunto como mejor combinacion para luego imprimirlo
        self.MejorCombinacion = subConjunto

    def BusquedaGredy(self):
        #Setea MejorCombinacion segun algoritmo de greedy
        self.SetMejorCombinacionPorGreedy()
        #Imprime valores obtenidos
        self.PrintMejorCombinacion()
