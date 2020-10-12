# Importamos las funciones para obtener numeros aleatorios
from random import randint, uniform, random, choice
import matplotlib.image as mpimg
import numpy as np

from TP_Investigacion_Fractales.Cromosoma import Cromosoma
from TP_Investigacion_Fractales.ImagenHelper import generate_all_transformed_blocks, reduce
from TP_Investigacion_Fractales.Poblacion import Poblacion


# De la lista de cromosomas que recive devuelve uno tomado al azar
# Simplemente toma un valor entero al azar y devuelve el objeto en ese indice
def SeleccionarCromosomaAlAzar(cromosomas: []) -> Cromosoma:
    numero = randint(0, len(cromosomas) - 1)
    return cromosomas[numero]


# Clase principal de nuestro programa
class AlgoritmoGenetico:

    # Iniciacion de variables, recive el objeto configuracion que contiene la parametrizacion de nuestro programa
    def __init__(self, configuracion):
        self.Configuracion = configuracion
        self.Poblaciones = []
        self.PoblacionActual = []
        self.Image = None
        self.LoadSourceImage()
        self.Transformed_blocks = generate_all_transformed_blocks(self.Image, self.Configuracion.Source_Size,
                                                                  self.Configuracion.Destination_Size,
                                                                  self.Configuracion.Step)
        self.i_count = self.Image.shape[0] // self.Configuracion.Destination_Size
        self.j_count = self.Image.shape[1] // self.Configuracion.Destination_Size

    # Metodo principal que realiza las iteraciones del programa
    def Run(self,ventana=None):

        self.Poblaciones.append(self.GetPoblacionInicial())
        for i in range(self.Configuracion.Iteraciones):
            if (ventana is not None):
                ventana.progress['value'] += (100 / self.Configuracion.Iteraciones)
                ventana.update_idletasks()
            print('Iteración número ' + str(i + 1))
            self.PoblacionActual = self.Poblaciones[len(self.Poblaciones) - 1]
            # Desmarca e inicializa valores de los cromosomas para evitar valores por referencias y resetear los
            # cromosomas elites
            for cromosoma in self.PoblacionActual.Cromosomas:
                cromosoma.Reset()
            nuevaPoblacion: Poblacion = self.PoblacionActual
            # Realiza la logica de elite si asi se deseo correr
            if self.Configuracion.Elite:
                nuevaPoblacion = self.Elite(nuevaPoblacion)
            nuevaPoblacion = self.SeleccionRuleta(nuevaPoblacion)
            nuevaPoblacion = self.Crossover(nuevaPoblacion)
            self.Mutacion(nuevaPoblacion)
            self.Poblaciones.append(nuevaPoblacion)

    def LoadSourceImage(self):
        if self.Configuracion.IsRGB:
            self.Image = mpimg.imread(self.Configuracion.ImagePath)
        else:
            self.Image = np.mean(mpimg.imread(self.Configuracion.ImagePath)[:, :, :2], 2)
            # self.Image = reduce(self.Image, self.Configuracion.Destination_Size)

    def GetPoblacionInicial(self) -> Poblacion:
        """Genera y devuelve la poblacion inicial dividiendo a la imagen en n bloques del mismo tamaño y guardando
           información relevante a ellos en los cromosomas de dicha población."""
        print('Generando Poblacion Inicial')
        poblacion = Poblacion()
        while len(poblacion.Cromosomas) != self.Configuracion.CantidadPoblacionInicial:
            print('Generando Cromosoma: ' + repr(len(poblacion.Cromosomas)) + '/' + repr(
                self.Configuracion.CantidadPoblacionInicial))
            poblacion.Cromosomas.append(
                Cromosoma().CargarTransformacionesAleatorias(self.Transformed_blocks, self.i_count, self.j_count,
                                                             self.Image, self.Configuracion.Destination_Size))
        print('Población inicial generada')
        return poblacion

    def FuncionObjetivo(self, c: Cromosoma):
        return c.FuncionObjetivo(self.Image, self.Configuracion.Source_Size, self.Configuracion.Destination_Size,
                                 self.Configuracion.Step)

    # Forma de calcular el fitness de cada cromosoma
    # Funcion objetiva de dicho cromosoma sobre la suma la funcion objetivo de cada cromosoma de la poblacion
    def FuncionFitness(self, cromosoma: Cromosoma):
        return 1 / self.FuncionObjetivo(cromosoma)

    def SeleccionRuleta(self, poblacionInicial: Poblacion) -> Poblacion:
        porciones = []
        nuevaPoblacion = Poblacion()

        elite = list(filter(lambda c: c.EsElite is True, poblacionInicial.Cromosomas))
        for cromosomaElite in elite:
            nuevaPoblacion.Cromosomas.append(cromosomaElite.Clone())

        for cromosoma in poblacionInicial.Cromosomas:
            if len(porciones) == 0:
                valorMinimo = 0
            else:
                valorMinimo = porciones[len(porciones) - 1].ValorMaximo
            valorMaximo = valorMinimo + self.FuncionFitness(cromosoma)
            cromosoma.PorcionRuleta.ValorMinimo = valorMinimo
            cromosoma.PorcionRuleta.ValorMaximo = valorMaximo
            porciones.append(cromosoma.PorcionRuleta)

        for i in range(self.Configuracion.CantidadPoblacionInicial - len(elite)):
            numero = uniform(0, porciones[len(porciones) - 1].ValorMaximo)
            lista = list(filter(
                lambda c: c.PorcionRuleta.ValorMinimo <= numero < c.PorcionRuleta.ValorMaximo,
                poblacionInicial.Cromosomas))
            nuevaPoblacion.Cromosomas.append(lista[0].Clone())
        return nuevaPoblacion

    def Elite(self, poblacionInicial: Poblacion) -> Poblacion:
        candidates = []
        noElite = list(filter(lambda cd: cd.EsElite is False, poblacionInicial.Cromosomas))
        for cromosoma in noElite:
            fitness = self.FuncionFitness(cromosoma)
            candidates.append((fitness, cromosoma))
        sorted(candidates, key=lambda candidate: candidate[0], reverse=True)

        for i in range(self.Configuracion.CantidadElites):
            candidates[i][1].Elite()
        return poblacionInicial

    def AplicarCrossover(self, cromosoma1: Cromosoma, cromosoma2: Cromosoma):
        corte = randint(0, len(cromosoma1.Transformaciones) - 1)
        primeraParteCromosoma1 = cromosoma1.Transformaciones[:corte]
        primeraParteCromosoma2 = cromosoma2.Transformaciones[:corte]
        segundaParteCromosoma1 = cromosoma1.Transformaciones[corte:]
        segundaParteCromosoma2 = cromosoma2.Transformaciones[corte:]

        c1 = Cromosoma()
        c1.Transformaciones.extend(primeraParteCromosoma1)
        c1.Transformaciones.extend(segundaParteCromosoma2)

        c2 = Cromosoma()
        c2.Transformaciones.extend(primeraParteCromosoma2)
        c2.Transformaciones.extend(segundaParteCromosoma1)

        c1.RefreshValorObjetivo()
        c2.RefreshValorObjetivo()

        return c1, c2, corte

    # Obtiene un valor para ver si aplica o no crossover segun el porcentaje
    def AplicaCrossover(self):
        numero = random()
        if 0 <= numero <= self.Configuracion.ProbabilidadCrossover:
            return True
        else:
            return False

    def Crossover(self, poblacionInicial: Poblacion) -> Poblacion:
        nuevaPoblacion = Poblacion()
        elite = list(filter(lambda c: c.EsElite is True, poblacionInicial.Cromosomas))
        for i in elite:
            nuevaPoblacion.Cromosomas.append(i.Clone())
        while len(nuevaPoblacion.Cromosomas) < self.Configuracion.CantidadPoblacionInicial:
            cromosoma1: Cromosoma = SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas).Clone()
            cromosoma2: Cromosoma = SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas).Clone()
            if not self.AplicaCrossover():
                nuevaPoblacion.Cromosomas.append(cromosoma1.Clone())
                nuevaPoblacion.Cromosomas.append(cromosoma2.Clone())
            else:
                hijos = self.AplicarCrossover(cromosoma1, cromosoma2)
                nuevaPoblacion.Cromosomas.append(hijos[0])
                nuevaPoblacion.Cromosomas.append(hijos[1])

        return nuevaPoblacion

    def Mutacion(self, poblacionInicial: Poblacion):
        """Recorre los cromosomas no elites de una poblacion y evalua si debe aplicar mutacion"""
        cromosomasNoElites = list(filter(lambda c: c.EsElite is False, poblacionInicial.Cromosomas))
        for cromosoma in cromosomasNoElites:
            if 0 <= random() <= self.Configuracion.ProbabilidadMutacion:
                cromosoma.Mutar(self.Image, self.Configuracion.Step, self.Configuracion.Source_Size,
                                self.Configuracion.Source_Size // self.Configuracion.Destination_Size)

    def GetMejorCromosoma(self) -> Cromosoma:
        mejorFitnes = self.FuncionFitness(self.Poblaciones[0].Cromosomas[0])
        mejorCromosoma = self.Poblaciones[0].Cromosomas[0]
        for poblacion in self.Poblaciones:
            for cromosoma in poblacion.Cromosomas:
                fitnes = self.FuncionFitness(cromosoma)
                if fitnes > mejorFitnes:
                    mejorFitnes = fitnes
                    mejorCromosoma = cromosoma
        return mejorCromosoma
