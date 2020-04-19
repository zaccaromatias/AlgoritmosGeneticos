from random import randint, uniform, random
from Ejercicio1.Crossover import Crossover
from Ejercicio1.Cromosoma import Cromosoma
from Ejercicio1.Poblacion import Poblacion
from Ejercicio1.Mutacion import Mutacion


class AlgoritmoGenetico:
    dominioInicial = 0
    dominioFinal = pow(2, 30) - 1

    def __init__(self, configuracion):
        self.Configuracion = configuracion
        self.Poblaciones = []

    def Run(self):
        for i in range(0, self.Configuracion.Iteraciones - 1):
            if i == 0:
                self.Poblaciones.append(self.GetPoblacionInicial())
            self.PoblacionActual = self.Poblaciones[len(self.Poblaciones) - 1]
            for cromosoma in self.PoblacionActual.Cromosomas:
                cromosoma.Reset()
            nuevaPoblacion = self.Seleccionar(self.PoblacionActual)
            nuevaPoblacion = self.EvaluarCrossover(nuevaPoblacion)
            self.EvaluarMutacion(nuevaPoblacion)
            self.Poblaciones.append(nuevaPoblacion)

    def GetPoblacionInicial(self) -> Poblacion:
        poblaicon = Poblacion()
        for i in range(self.Configuracion.CantidadPoblacionInicial):
            numeroRandom = randint(self.dominioInicial, self.dominioFinal)
            poblaicon.Cromosomas.append(Cromosoma(numeroRandom))
        return poblaicon

    def Seleccionar(self, poblacionInicial: Poblacion) -> Poblacion:
        return self.AplicarSeleccionRuedadeRuleta(poblacionInicial)

    def AplicarSeleccionRuedadeRuleta(self, poblacionInicial: Poblacion) -> Poblacion:
        ruleta = 360
        porciones = []
        nuevaPoblacion = Poblacion()
        for cromosoma in poblacionInicial.Cromosomas:
            valorMinimo = 0
            if len(porciones) > 0:
                valorMinimo = porciones[len(porciones) - 1].ValorMaximo
            valorMaximo = valorMinimo + (self.FuncionFitness(poblacionInicial, cromosoma) * ruleta)
            if (self.Configuracion.CantidadPoblacionInicial - len(porciones) == 1):
                valorMaximo = ruleta
            cromosoma.PorcionRuleta.ValorMinimo = valorMinimo
            cromosoma.PorcionRuleta.ValorMaximo = valorMaximo
            porciones.append(cromosoma.PorcionRuleta)

        for i in range(self.Configuracion.CantidadPoblacionInicial):
            numero = randint(0, ruleta)
            cromosomaSeleccionado = list(filter(
                lambda c: numero >= c.PorcionRuleta.ValorMinimo and numero <= c.PorcionRuleta.ValorMaximo,
                poblacionInicial.Cromosomas))[0]
            nuevaPoblacion.Cromosomas.append(Cromosoma(cromosomaSeleccionado.Valor))
        return nuevaPoblacion

    def EvaluarCrossover(self, poblacionInicial: Poblacion) -> Poblacion:
        nuevaPoblacion = Poblacion()
        noSeleccionados = list(filter(lambda c: c.YaSeleccionado == False, poblacionInicial.Cromosomas))
        while len(noSeleccionados) > 0:
            cromosoma1: Cromosoma = self.SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas)
            cromosoma2: Cromosoma = self.SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas)
            if self.AplicaCrossover():
                hijos = self.AplicarCrosOverDeTipoUnPunto(cromosoma1, cromosoma2)
                nuevaPoblacion.Cromosomas.append(hijos[0])
                nuevaPoblacion.Cromosomas.append(hijos[1])
                nuevaPoblacion.Crossovers.append(Crossover(cromosoma1, cromosoma2, hijos[0], hijos[1], hijos[2]))
            else:
                nuevaPoblacion.Cromosomas.append(cromosoma1)
                nuevaPoblacion.Cromosomas.append(cromosoma2)
            noSeleccionados = list(filter(lambda c: c.YaSeleccionado == False, poblacionInicial.Cromosomas))
        return nuevaPoblacion

    def SeleccionarCromosomaAlAzar(self, cromosomas: []) -> Cromosoma:
        posibles: [] = list(filter(lambda c: c.YaSeleccionado == False, cromosomas))
        if (len(posibles) == 1):
            return posibles[0].Seleccionar()
        numero = randint(0, len(posibles) - 1)
        return posibles[numero].Seleccionar()

    def AplicaCrossover(self):
        numero = uniform(0, 100)
        if (numero >= 0 and numero <= (self.Configuracion.ProbabilidadCrossover * 100)):
            ##print(str(numero) + " <= " + str((self.Configuracion.ProbabilidadCrossover * 100)))
            return True
        return False

    def AplicarCrosOverDeTipoUnPunto(self, cromosoma1: Cromosoma, cromosoma2: Cromosoma):
        binario1 = format(cromosoma1.Valor, "b")
        binario2 = format(cromosoma2.Valor, "b")
        unidades = randint(0, len(binario1) - 1)
        primeraParteBinario1 = binario1[:unidades]
        primeraParteBinario2 = binario2[:unidades]
        segundaParteBinario1 = binario1[unidades:]
        segundaParteBinario2 = binario2[unidades:]
        nuevoBinario1 = primeraParteBinario1 + segundaParteBinario2
        nuevoBinario2 = primeraParteBinario2 + segundaParteBinario1
        return Cromosoma(int(nuevoBinario1, 2)), Cromosoma(int(nuevoBinario2, 2)), unidades

    def AplicaMutacion(self):
        numero = uniform(0, 100)
        if (numero >= 0 and numero <= (self.Configuracion.ProbabilidadMutacion * 100)):
            print(str(numero) + " <= " + str((self.Configuracion.ProbabilidadMutacion * 100)))
            return True
        return False

    def EvaluarMutacion(self, poblacionInicial: Poblacion):
        for cromosoma in poblacionInicial.Cromosomas:
            if (self.AplicaMutacion() == True):
                self.AplicarMutacion(poblacionInicial, cromosoma)

    def AplicarMutacion(self, poblacion: Poblacion, cromosoma: Cromosoma):
        mutacion = Mutacion(cromosoma.Clone())
        binario = list(format(cromosoma.Valor, "b"))
        numero = randint(0, len(binario) - 1)
        if binario[numero] == "0":
            binario[numero] = "1"
        else:
            binario[numero] = "0"
        nuevo = int("".join(binario), 2)
        cromosoma.Valor = nuevo
        mutacion.Mutante = cromosoma
        mutacion.IndiceBitCambiado = numero
        poblacion.Mutaciones.append(mutacion)

    def FuncionFitness(self, poblacionInicial: Poblacion, cromosoma: Cromosoma):
        return self.FuncionObjetivo(cromosoma.Valor) / sum(
            self.FuncionObjetivo(c.Valor) for c in poblacionInicial.Cromosomas)

    def FuncionObjetivo(self, valor):
        return pow(valor / (pow(2, 30) - 1), 2)

    def Print(self):
        iteracion = 1
        for poblacion in self.Poblaciones:
            print("*******Poblacion Numero: " + str(iteracion))
            poblacion.Print(self.FuncionObjetivo, self.FuncionFitness, self.Configuracion.PrintCrossovers,
                            self.Configuracion.PrintMutaciones)
            iteracion = iteracion + 1
        ideal = pow(2, 30) - 1
        print()
        print()
        print("******* El Ideal que sabemos: " + str(ideal) + " -- Objetivo: " + str(self.FuncionObjetivo(ideal)))
