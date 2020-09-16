from Ejercicio3.Cromosoma import Cromosoma


# Clase que representa una poblacion con su lista de cromosomas
# Ademas solo por mera informacion contiene los crossovers y mutaciones realizados
class Poblacion:
    def __init__(self):
        self.Cromosomas = []
        self.Mutaciones = []
        self.Crossovers = []

    # Devuelve el maximo cromosoma segun su funcion objetivo
    def Maximo(self, funcionObjetivo) -> Cromosoma:
        valorMaximo = min(funcionObjetivo(cromosoma) for cromosoma in self.Cromosomas)
        maximo = list(filter(lambda c: funcionObjetivo(c) == valorMaximo, self.Cromosomas))
        return maximo[0]

    # Devuelve el minimo cromosoma segun su funcion objetivo
    def Minimo(self, funcionObjetivo) -> Cromosoma:
        valorminimo = min(funcionObjetivo(cromosoma) for cromosoma in self.Cromosomas)
        minimo = list(filter(lambda c: funcionObjetivo(c) == valorminimo, self.Cromosomas))
        return minimo[0]

    # Retorna el promedio objetivo de dicha poblacion
    def Promedio(self, funcionObjetivo):
        return sum(funcionObjetivo(cromosoma) for cromosoma in self.Cromosomas) / len(self.Cromosomas)

    # Metodos para mostrar resultados en pantallas
    def PrintCrossovers(self):
        print("/////Crosovers: " + str(len(self.Crossovers)))
        for cross in self.Crossovers:
            cross.MyPrint()

    def PrintMutaciones(self):
        print("/////Mutaciones: " + str(len(self.Mutaciones)))
        for mutacion in self.Mutaciones:
            mutacion.MyPrint()

    def PrintCromosomas(self, FuncionObjetivo, FuncionFitness):
        for cromosoma in self.Cromosomas:
            print("Valor: " + str(cromosoma.Distancia()) + " -- Objetivo: " + str(FuncionObjetivo(
                cromosoma)) + " -- Fitness: " + str(FuncionFitness(cromosoma)))

    def PrintPromedio(self, FuncionObjetivo):
        print("----Promedio :" + str(self.Promedio(FuncionObjetivo)))

    def PrintMaximo(self, FuncionObjetivo, FuncionFitness):
        maximo = self.Maximo(FuncionObjetivo)
        print("----Maximo: " + str(maximo) + " -- Objetivo: " + str(FuncionObjetivo(
            maximo)) + " -- Fitness: " + str(FuncionFitness(maximo)))

    def PrintMinimo(self, FuncionObjetivo, FuncionFitness):
        minimo = self.Minimo(FuncionObjetivo)
        print("----Minimo: " + str(minimo) + " -- Objetivo: " + str(FuncionObjetivo(
            minimo)) + " -- Fitness: " + str(FuncionFitness(minimo)))

    def Print(self, FuncionObjetivo, FuncionFitness):
        self.PrintCromosomas(FuncionObjetivo, FuncionFitness)
        self.PrintCrossovers()
        self.PrintMutaciones()
        self.PrintMaximo(FuncionObjetivo, FuncionFitness)
        self.PrintMinimo(FuncionObjetivo, FuncionFitness)
        self.PrintPromedio(FuncionObjetivo)
