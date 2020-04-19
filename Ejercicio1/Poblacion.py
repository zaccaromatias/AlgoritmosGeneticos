from Ejercicio1.Cromosoma import Cromosoma


class Poblacion:
    def __init__(self):
        self.Cromosomas = []
        self.Mutaciones = []
        self.Crossovers = []

    def Maximo(self) -> Cromosoma:
        valorMaximo = max(cromosoma.Valor for cromosoma in self.Cromosomas)
        maximo = list(filter(lambda c: c.Valor == valorMaximo, self.Cromosomas))
        return maximo[0]

    def Minimo(self) -> Cromosoma:
        valorminimo = min(cromosoma.Valor for cromosoma in self.Cromosomas)
        minimo = list(filter(lambda c: c.Valor == valorminimo, self.Cromosomas))
        return minimo[0]

    def Promedio(self, funcionObjetivo):
        return sum(funcionObjetivo(cromosoma.Valor) for cromosoma in self.Cromosomas) / len(self.Cromosomas)

    def PrintCrossovers(self):
        print("/////Crosovers: " + str(len(self.Crossovers)))
        for cross in self.Crossovers:
            cross.MyPrint()

    def PrintMutaciones(self):
        print("/////Mutaciones: " + str(len(self.Mutaciones)))
        for mutacion in self.Mutaciones:
            mutacion.MyPrint()

    def PrintCromosomoas(self, FuncionObjetivo, FuncionFitness):
        for cromosoma in self.Cromosomas:
            print("Valor: " + str(cromosoma.Valor) + " -- Objetivo: " + str(FuncionObjetivo(
                cromosoma.Valor)) + " -- Fitness: " + str(FuncionFitness(self, cromosoma)))

    def PrintPromedio(self, FuncionObjetivo):
        print("----Promedio :" + str(self.Promedio(FuncionObjetivo)))

    def PrintMaximo(self, FuncionObjetivo, FuncionFitness):
        maximo = self.Maximo()
        print("----Maximo: " + str(maximo.Valor) + " -- Objetivo: " + str(FuncionObjetivo(
            maximo.Valor)) + " -- Fitness: " + str(FuncionFitness(self, maximo)))

    def PrintMinimo(self, FuncionObjetivo, FuncionFitness):
        minimo = self.Minimo()
        print("----Minimo: " + str(minimo.Valor) + " -- Objetivo: " + str(FuncionObjetivo(
            minimo.Valor)) + " -- Fitness: " + str(FuncionFitness(self, minimo)))

    def Print(self, FuncionObjetivo, FuncionFitness, printCrossovers: bool, printMutaciones: bool):
        self.PrintCromosomoas(FuncionObjetivo, FuncionFitness)
        if (printCrossovers == True):
            self.PrintCrossovers()
        if (printMutaciones == True):
            self.PrintMutaciones()
        self.PrintMaximo(FuncionObjetivo, FuncionFitness)
        self.PrintMinimo(FuncionObjetivo, FuncionFitness)
        self.PrintPromedio(FuncionObjetivo)
