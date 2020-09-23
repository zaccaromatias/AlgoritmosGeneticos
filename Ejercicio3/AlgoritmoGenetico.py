# Importamos las funciones para obtener numeros aleatorios
from random import randint, uniform, random, shuffle

from Ejercicio3 import DistanciaHelper
from Ejercicio3.Cromosoma import Cromosoma
from Ejercicio3.Crossover import Crossover
from Ejercicio3.Poblacion import Poblacion
from Ejercicio3.DistanciaHelper import DistanciaHelper

"""Realiza el crossover usando el metodo cicliclo pero teniendo en cuenta un unico ciclo. Especificado en el apunte 
de la catedra"""


def AplicarCrossoverCiclico(padre1: Cromosoma, padre2: Cromosoma):
    # Arranca del primer gen(primera ciudad) del padre 1
    indice = 0
    indicesDeGenesQueNoCambian = []
    # Ciudad inicial
    ciudadInicial = padre1.Ciudades[indice]
    # Ciudad del padre 2 en el mismo indice
    ciudadEnPadre2 = padre2.Ciudades[indice]
    # Agrega el indice inicial
    indicesDeGenesQueNoCambian.append(indice)
    # Mientras la ciudadEnPadre2 difiera de la ciudadInicial continua con el ciclo
    while ciudadEnPadre2 != ciudadInicial:
        # Busca el indice de la ciudadEnPadre2  en el padre 1 y devuelve lo que hay en el padre 2 en ese indice
        indice = padre1.Ciudades.index(ciudadEnPadre2)
        ciudadEnPadre2 = padre2.Ciudades[indice]
        # Agrega indice que no va a cambiar
        indicesDeGenesQueNoCambian.append(indice)
    # Inicio arrays
    hijo1 = []
    hijo2 = []
    # Loop de 0 a cantidad de ciudades.
    # si el indice que esta recorriendo no esta en el array de indicesDeGenesQueNoCambian los invierte
    # En caso que esten quedan las mismas
    for i in range(len(padre1.Ciudades)):
        if i in indicesDeGenesQueNoCambian:
            hijo1.append(padre1.Ciudades[i])
            hijo2.append(padre2.Ciudades[i])
        else:
            hijo1.append(padre2.Ciudades[i])
            hijo2.append(padre1.Ciudades[i])
    # Retorna una tupla de 3 valores los primeros dos lugares son los nuevos cromosomas
    # El 3er valor es meramente informativo no tiene importancia es la cantidad de ciclos pero en este caso siempre es 1
    return Cromosoma(hijo1), Cromosoma(hijo2), 1


def AplicarCrossoverCiclicoMultiple(padre1: Cromosoma, padre2: Cromosoma):
    """Define los ciclos y luego aplica el crossover entre dos cromosomas padres.
    Devuelve dos cromosomas hijos y la cantidad de ciclos"""

    # Inicializo las listas que devuelve el método al final
    ciclos = []
    hijo1 = [0 for x in range(24)]
    hijo2 = list.copy(hijo1)

    # Este bucle recorre las capitales del primer padre en orden ascendente y revisa que ella no se encuentre en un
    # ciclo ya existente para evitar agregar ciclos repetidos.
    for i in range(len(padre1.Ciudades)):
        nuevoCiclo = True
        for k in range(len(ciclos)):
            if len(ciclos) == 0:
                break
            for j in range(len(ciclos[k]) - 1):
                if ciclos[k][j] == i:
                    nuevoCiclo = False
                    break

        # Registro de un nuevo ciclo: Busca los lugares de las listas de ciudades en ambos cromosomas (comenzando por el
        # primero) para encontrar el ciclo correspondiente a ellas.
        if nuevoCiclo:
            ciclo = []
            indicePadre1 = i
            ciclo.append(indicePadre1)
            indicePadre2 = -1  # <- Valor dummy para poder entrar al bucle
            while i != indicePadre2:
                indicePadre2 = padre2.Ciudades.index(padre1.Ciudades[indicePadre1])
                ciclo.append(indicePadre2)
                if ciclo[len(ciclo) - 1] == ciclo[0]:
                    ciclo.remove(ciclo[len(ciclo) - 1])  # <- Para que el primer elemento del ciclo no aparezca repetido
                    break
                indicePadre1 = indicePadre2
            ciclos.append(ciclo)  # <- Se agrega el ciclo actual a la lista de ciclos

    # Una vez completa la lista de ciclos, se procede al proceso de crossover donde se intercambian los genes para
    # formar los nuevos cromosomas hijos. En el primer ciclo, el primer padre da sus genes al primer hijo y el segundo
    # al segundo. En el segundo ciclo, el primer padre da sus genes al segundo hijo, y el segundo al primero. Y así
    # sucesivamente.
    for n in range(len(ciclos)):
        for m in range(len(ciclos[n])):
            if n % 2 == 0:
                hijo1[ciclos[n][m]] = padre1.Ciudades[ciclos[n][m]]
                hijo2[ciclos[n][m]] = padre2.Ciudades[ciclos[n][m]]
            else:
                hijo1[ciclos[n][m]] = padre2.Ciudades[ciclos[n][m]]
                hijo2[ciclos[n][m]] = padre1.Ciudades[ciclos[n][m]]

    return Cromosoma(hijo1), Cromosoma(hijo2), len(ciclos)


def SeleccionarCromosomaAlAzar(cromosomas: []) -> Cromosoma:
    """De la lista de cromosomas que recibe, devuelve uno tomado al azar"""
    numero = randint(0, len(cromosomas) - 1)
    return cromosomas[numero]


def FuncionFitness(cromosoma: Cromosoma):
    """Calcula y devuelve el fitness de un cromosoma determinado (1/Distancia)"""
    return 1 / FuncionObjetivo(cromosoma)


def FuncionObjetivo(cromosoma: Cromosoma):
    return cromosoma.Distancia()


class AlgoritmoGenetico:
    # Iniciacion de variables, recive el objeto configuracion que contiene la paremetrizacion de nuestro programa
    def __init__(self, configuracion):
        self.Configuracion = configuracion
        self.Poblaciones = []
        self.PoblacionActual = []

    def Run(self, ventana=None):
        """Metodo principal que realiza las iteraciones del programa"""
        for i in range(self.Configuracion.Iteraciones):
            if (ventana is not None):
                ventana.progress['value'] += (100 / self.Configuracion.Iteraciones)
                ventana.update_idletasks()
            if i == 0:
                # Siendo la primera iteracion genera la poblacion inicial
                self.Poblaciones.append(self.GetPoblacionInicial())
            self.PoblacionActual = self.Poblaciones[len(self.Poblaciones) - 1]
            # Desmarca e inicializa valores de los cromosomas para evitar valores por referencias y resetear los
            # cromosomas elites
            for cromosoma in self.PoblacionActual.Cromosomas:
                cromosoma.Reset()
            nuevaPoblacion: Poblacion = self.PoblacionActual
            # Realiza la logica de elite si asi se deseo correr
            if self.Configuracion.Elite:
                nuevaPoblacion = self.Elite(nuevaPoblacion)
            nuevaPoblacion = self.AplicarSeleccionRuedadeRuleta(nuevaPoblacion)
            nuevaPoblacion = self.EvaluarCrossover(nuevaPoblacion)
            self.EvaluarMutacion(nuevaPoblacion)
            self.Poblaciones.append(nuevaPoblacion)

    def GetPoblacionInicial(self) -> Poblacion:
        """Crea la población inicial generando cromosomas con valores binarios totalmente aleatorios"""
        poblacion = Poblacion()
        for i in range(self.Configuracion.NumeroCromosomasPoblacion):
            capitales = DistanciaHelper.Capitales.copy()
            # Las desordena al azar
            shuffle(capitales)
            poblacion.Cromosomas.append(Cromosoma(capitales))
        return poblacion

    def AplicarSeleccionRuedadeRuleta(self, poblacionInicial: Poblacion) -> Poblacion:
        """Lógica de selección de cromosomas a través del método de la ruleta"""
        porciones = []
        nuevaPoblacion = Poblacion()
        # Segun el fitnes de cada cromosomas le seteamos los valores Minimos y maximos de la porcion que ocuparian
        # (entre 0 y 1) acumulamos
        # Seleccionamos un numero decimal aleatorio entre 0 y 1 y verificamos a que cromosoma corresponde segun su porcion
        # Asi hasta completar poblacion
        elite = list(filter(lambda c: c.EsElite is True, poblacionInicial.Cromosomas))
        for cromosomaElite in elite:
            nuevaPoblacion.Cromosomas.append(cromosomaElite.Clone())

        for cromosoma in poblacionInicial.Cromosomas:
            if len(porciones) == 0:
                valorMinimo = 0
            else:
                valorMinimo = porciones[len(porciones) - 1].ValorMaximo
            valorMaximo = valorMinimo + FuncionFitness(cromosoma)
            cromosoma.PorcionRuleta.ValorMinimo = valorMinimo
            cromosoma.PorcionRuleta.ValorMaximo = valorMaximo
            porciones.append(cromosoma.PorcionRuleta)

        for i in range(self.Configuracion.NumeroCromosomasPoblacion - len(elite)):
            numero = uniform(0, porciones[len(porciones) - 1].ValorMaximo)
            lista = list(filter(
                lambda c: c.PorcionRuleta.ValorMinimo <= numero < c.PorcionRuleta.ValorMaximo,
                poblacionInicial.Cromosomas))
            nuevaPoblacion.Cromosomas.append(lista[0].Clone())
        return nuevaPoblacion

    # Logica para marcar los mejores X cromosomas segun su fitness
    # Recorre X veces buscando el mayor fitness entre los Cromosomas que no son elites
    # Luego el cromosoma correspondiente para marcarlo como elite
    def Elite(self, poblacionInicial: Poblacion) -> Poblacion:
        countTrue = 0
        while countTrue < self.Configuracion.CantidadElites:
            minimaDistancia = max(
                [FuncionFitness(c) for c in
                 filter(lambda cd: cd.EsElite is False, poblacionInicial.Cromosomas)])
            best = \
                list(filter(lambda cd: cd.EsElite is False and FuncionFitness(cd) == minimaDistancia,
                            poblacionInicial.Cromosomas))[0]
            best.Elite()
            countTrue += 1
        return poblacionInicial

    # Recorre los cromosomas de la poblacion
    # Para ir seleccionando parejas para ver si aplica crosovers o no
    # En caso de hacerlo llama a la logica agrega los cromosomas hijos de la cruza
    # Y a modo informativo los va guardando en una coleccion
    # En caso de no aplicar crossover pasa dicha pareja de cromosomas a la nueva poblacion
    # y en caso de los cromosomas Elites los pasa directamente
    def EvaluarCrossover(self, poblacionInicial: Poblacion) -> Poblacion:
        nuevaPoblacion = Poblacion()
        elite = list(filter(lambda c: c.EsElite is True, poblacionInicial.Cromosomas))
        for i in elite:
            nuevaPoblacion.Cromosomas.append(i.Clone())
        while len(nuevaPoblacion.Cromosomas) < self.Configuracion.NumeroCromosomasPoblacion:
            cromosoma1: Cromosoma = SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas).Clone()
            cromosoma2: Cromosoma = SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas).Clone()
            if self.AplicaCrossover():
                if self.Configuracion.DiversidadGenetica:
                    hijos = AplicarCrossoverCiclicoMultiple(cromosoma1, cromosoma2)
                    nuevaPoblacion.Cromosomas.append(hijos[0])
                    nuevaPoblacion.Cromosomas.append(hijos[1])
                    nuevaPoblacion.Crossovers.append(Crossover(cromosoma1, cromosoma2, hijos[0], hijos[1], hijos[2]))
                else:
                    hijos = AplicarCrossoverCiclico(cromosoma1, cromosoma2)
                    nuevaPoblacion.Cromosomas.append(hijos[0])
                    nuevaPoblacion.Cromosomas.append(hijos[1])
                    nuevaPoblacion.Crossovers.append(Crossover(cromosoma1, cromosoma2, hijos[0], hijos[1], hijos[2]))
            else:
                nuevaPoblacion.Cromosomas.append(cromosoma1.Clone())
                nuevaPoblacion.Cromosomas.append(cromosoma2.Clone())
        return nuevaPoblacion

    # Obtiene un valor para ver si aplica o no crossover segun el porcentaje
    def AplicaCrossover(self):
        numero = random()
        if 0 <= numero <= self.Configuracion.ProbabilidadCrossover:
            return True
        else:
            return False

    # Obtiene un valor para ver si aplica o no Mutacion segun el porcentaje
    def AplicaMutacion(self):
        numero = random()
        if 0 <= numero <= self.Configuracion.ProbabilidadMutacion:
            return True
        else:
            return False

    # Recorre los cromosomas no elites de una poblacion y evalua si debe aplciar mutacion
    def EvaluarMutacion(self, poblacionInicial: Poblacion):
        cromosomasNoElites = list(filter(lambda c: c.EsElite is False, poblacionInicial.Cromosomas))
        for cromosoma in cromosomasNoElites:
            if self.AplicaMutacion():
                poblacionInicial.Mutaciones.append(cromosoma.Mutar())

    # Devuelve el cromosoma con el valor objetivo maximo obtenido
    def GetMejorCromosomaDeTodasLasPoblaciones(self):
        mejores = []
        iteracion = 1
        # En este caso el mejor el que tenga menor funcion objetivo
        for poblacion in self.Poblaciones:
            mejores.append([iteracion, poblacion.Minimo(FuncionObjetivo)])
            iteracion += 1
        mejorValor = max(FuncionFitness(cromosoma[1]) for cromosoma in mejores)
        mejorDeLosMejores = list(filter(lambda c: FuncionFitness(c[1]) == mejorValor, mejores))[0]
        return mejorDeLosMejores
