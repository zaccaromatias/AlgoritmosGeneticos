from random import randint, uniform, random

import datetime
import os
import xlsxwriter

from Ejercicio1.Cromosoma import Cromosoma
from Ejercicio1.Crossover import Crossover
from Ejercicio1.Mutacion import Mutacion
from Ejercicio1.Poblacion import Poblacion


def AplicarCrosOverDeTipoUnPunto(cromosoma1: Cromosoma, cromosoma2: Cromosoma):
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


def SeleccionarCromosomaAlAzar(cromosomas: []) -> Cromosoma:
    posibles = list(filter(lambda c: c.YaSeleccionado == False, cromosomas))
    if len(posibles) == 1:
        return posibles[0].Seleccionar()
    numero = randint(0, len(posibles) - 1)
    return posibles[numero].Seleccionar()


def AplicarMutacion(poblacion: Poblacion, cromosoma: Cromosoma):
    mutacion = Mutacion(cromosoma.Clone())
    binario = list(format(cromosoma.Valor, "b"))
    numeroBit = randint(0, len(binario) - 1)
    if binario[numeroBit] == "0":
        binario[numeroBit] = "1"
    else:
        binario[numeroBit] = "0"
    nuevo = int("".join(binario), 2)
    cromosoma.Valor = nuevo
    mutacion.Mutante = cromosoma
    mutacion.IndiceBitCambiado = numeroBit
    poblacion.Mutaciones.append(mutacion)


def FuncionObjetivo(valor):
    return pow(valor / (pow(2, 30) - 1), 2)


def FuncionFitness(poblacionInicial: Poblacion, cromosoma: Cromosoma):
    return FuncionObjetivo(cromosoma.Valor) / sum(
        FuncionObjetivo(c.Valor) for c in poblacionInicial.Cromosomas)


class AlgoritmoGenetico:
    dominioFinal = 30

    def __init__(self, configuracion):
        self.Configuracion = configuracion
        self.Poblaciones = []
        self.PoblacionActual = []

    def Run(self):
        for i in range(self.Configuracion.Iteraciones):
            if i == 0:
                self.Poblaciones.append(self.GetPoblacionInicial())
            self.PoblacionActual = self.Poblaciones[len(self.Poblaciones) - 1]
            for cromosoma in self.PoblacionActual.Cromosomas:
                cromosoma.Reset()
            nuevaPoblacion = self.Seleccionar(self.PoblacionActual)
            if self.Configuracion.Elite:
                nuevaPoblacion = self.Elite(nuevaPoblacion)
            nuevaPoblacion = self.EvaluarCrossover(nuevaPoblacion)
            self.EvaluarMutacion(nuevaPoblacion)
            self.Poblaciones.append(nuevaPoblacion)

    def GetPoblacionInicial(self) -> Poblacion:
        poblacion = Poblacion()
        for i in range(self.Configuracion.CantidadPoblacionInicial):
            numeroRandom = ""
            for j in range(self.dominioFinal):
                numeroRandom += str(randint(0, 1))
            poblacion.Cromosomas.append(Cromosoma(int(numeroRandom, 2)))
        return poblacion

    def Seleccionar(self, poblacionInicial: Poblacion) -> Poblacion:
        return self.AplicarSeleccionRuedadeRuleta(poblacionInicial)

    def AplicarSeleccionRuedadeRuleta(self, poblacionInicial: Poblacion) -> Poblacion:
        porciones = []
        nuevaPoblacion = Poblacion()
        for cromosoma in poblacionInicial.Cromosomas:
            if len(porciones) == 0:
                valorMinimo = 0
            else:
                valorMinimo = porciones[len(porciones) - 1].ValorMaximo
            valorMaximo = valorMinimo + FuncionFitness(poblacionInicial, cromosoma)
            if len(porciones) == self.Configuracion.CantidadPoblacionInicial - 1:
                valorMaximo = 1
            cromosoma.PorcionRuleta.ValorMinimo = valorMinimo
            cromosoma.PorcionRuleta.ValorMaximo = valorMaximo
            porciones.append(cromosoma.PorcionRuleta)

        for i in range(self.Configuracion.CantidadPoblacionInicial):
            numero = random()
            lista = list(filter(
                lambda c: c.PorcionRuleta.ValorMinimo <= numero <= c.PorcionRuleta.ValorMaximo,
                poblacionInicial.Cromosomas))
            cromosomaSeleccionado = lista[0]
            nuevaPoblacion.Cromosomas.append(Cromosoma(cromosomaSeleccionado.Valor))
        return nuevaPoblacion

    def Elite(self, poblacionInicial: Poblacion) -> Poblacion:
        countTrue = 0
        while countTrue < 2:
            elite = 0
            noElite = list(filter(lambda cd: cd.Elite == False, poblacionInicial.Cromosomas))
            for cromosoma in noElite:
                if FuncionFitness(poblacionInicial, cromosoma) > elite:
                    elite = FuncionFitness(poblacionInicial, cromosoma)
            for cromosoma in noElite:
                if FuncionFitness(poblacionInicial, cromosoma) == elite and countTrue < 2:
                    Cromosoma.Elite(cromosoma)
                    countTrue += 1
        return poblacionInicial

    def EvaluarCrossover(self, poblacionInicial: Poblacion) -> Poblacion:
        nuevaPoblacion = Poblacion()
        noSeleccionados = list(filter(lambda c: c.YaSeleccionado == False and c.Elite == False,
                                      poblacionInicial.Cromosomas))
        while len(noSeleccionados) > 0:
            cromosoma1: Cromosoma = SeleccionarCromosomaAlAzar(noSeleccionados)
            noSeleccionados = list(filter(lambda c: c.YaSeleccionado == False,
                                          noSeleccionados))
            cromosoma2: Cromosoma = SeleccionarCromosomaAlAzar(noSeleccionados)
            if self.AplicaCrossover():
                hijos = AplicarCrosOverDeTipoUnPunto(cromosoma1, cromosoma2)
                nuevaPoblacion.Cromosomas.append(hijos[0])
                nuevaPoblacion.Cromosomas.append(hijos[1])
                nuevaPoblacion.Crossovers.append(Crossover(cromosoma1, cromosoma2, hijos[0], hijos[1], hijos[2]))
            else:
                nuevaPoblacion.Cromosomas.append(cromosoma1)
                nuevaPoblacion.Cromosomas.append(cromosoma2)
            noSeleccionados = list(filter(lambda c: c.YaSeleccionado == False,
                                          noSeleccionados))
        elite = list(filter(lambda c: c.Elite == True, poblacionInicial.Cromosomas))
        for i in elite:
            nuevaPoblacion.Cromosomas.append(i)
        return nuevaPoblacion

    def AplicaCrossover(self):
        numero = uniform(0, 1)
        if 0 <= numero <= self.Configuracion.ProbabilidadCrossover:
            return True
        else:
            return False

    def AplicaMutacion(self):
        numero = uniform(0, 1)
        if 0 <= numero <= self.Configuracion.ProbabilidadMutacion:
            print("MUTACIÓN")
            return True
        else:
            return False

    def EvaluarMutacion(self, poblacionInicial: Poblacion):
        poblacion = list(filter(lambda c: c.Elite == False, poblacionInicial.Cromosomas))
        for cromosoma in poblacion:
            if self.AplicaMutacion():
                AplicarMutacion(poblacionInicial, cromosoma)

    def Print(self):
        iteracion = 1
        for poblacion in self.Poblaciones:
            print("*******Poblacion Numero: " + str(iteracion))
            poblacion.Print(FuncionObjetivo, FuncionFitness)
            iteracion = iteracion + 1
        ideal = pow(2, 30) - 1
        print()
        print()
        print("******* El Ideal que sabemos: " + str(ideal) + " -- Objetivo: " + str(FuncionObjetivo(ideal)))
        print("******* Maximo Calculado: ")
        self.Poblaciones[len(self.Poblaciones) - 1].PrintMaximo(FuncionObjetivo, FuncionFitness)

# ----------------------------------------------------------------------------------------------------------------------

    def ExportToExcel(self):
        name = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.xlsx'
        # path = "" + name
        fullPath = 'E:/Apuntes UTN/III/Algoritmos Genéticos/Excels/' + name
        workbook = xlsxwriter.Workbook(fullPath)
        worksheetIteraciones = workbook.add_worksheet("Iteraciones")
        worksheetPromedios = workbook.add_worksheet("Promedios")
        worksheetMaximos = workbook.add_worksheet("Maximos")
        worksheetMinimos = workbook.add_worksheet("Minimos")
        worksheetCrossovers = workbook.add_worksheet("Crossovers")
        worksheetMutaciones = workbook.add_worksheet("Mutaciones")
        worksheetConfiguracion = workbook.add_worksheet("Configuracion")
        bold = workbook.add_format({'bold': 1})
        worksheetIteraciones.write('A1', 'Iteracion', bold)
        worksheetIteraciones.write('B1', 'Valor', bold)
        worksheetIteraciones.write('C1', 'Objetivo', bold)
        worksheetIteraciones.write('D1', 'Fitness', bold)

        worksheetPromedios.write('A1', 'Iteracion', bold)
        worksheetPromedios.write('B1', 'Promedio', bold)

        worksheetMaximos.write('A1', 'Iteracion', bold)
        worksheetMaximos.write('B1', 'Valor', bold)
        worksheetMaximos.write('C1', 'Objetivo', bold)
        worksheetMaximos.write('D1', 'Fitness', bold)

        worksheetMinimos.write('A1', 'Iteracion', bold)
        worksheetMinimos.write('B1', 'Valor', bold)
        worksheetMinimos.write('C1', 'Objetivo', bold)
        worksheetMinimos.write('D1', 'Fitness', bold)

        worksheetCrossovers.write('A1', 'Iteracion', bold)
        worksheetCrossovers.write('B1', 'Progenitor 1', bold)
        worksheetCrossovers.write('C1', 'Binario 1', bold)
        worksheetCrossovers.write('D1', 'Progenitor 2', bold)
        worksheetCrossovers.write('E1', 'Binario 2', bold)
        worksheetCrossovers.write('F1', 'Hijo 1', bold)
        worksheetCrossovers.write('G1', 'Binario Hijo 1', bold)
        worksheetCrossovers.write('H1', 'Hijo 2', bold)
        worksheetCrossovers.write('I1', 'Binario Hijo 2', bold)
        worksheetCrossovers.write('J1', 'Unidad Corte', bold)

        worksheetMutaciones.write('A1', 'Iteracion', bold)
        worksheetMutaciones.write('B1', 'Original', bold)
        worksheetMutaciones.write('C1', 'Original Binario', bold)
        worksheetMutaciones.write('D1', 'Mutante', bold)
        worksheetMutaciones.write('E1', 'Mutante Binario', bold)
        worksheetMutaciones.write('F1', 'Indice Cambiado', bold)

        iteracion = 1
        dataPromedios = []
        dataMaximos = []
        dataMinimos = []
        dataIteraciones = []
        dataCrosovers = []
        dataMutacion = []
        for poblacion in self.Poblaciones:
            for cromosoma in poblacion.Cromosomas:
                fila = [iteracion, cromosoma.Valor, FuncionObjetivo(cromosoma.Valor),
                        FuncionFitness(poblacion, cromosoma)]
                dataIteraciones.append(fila)
            for crossover in poblacion.Crossovers:
                dataCrosovers.append([iteracion, crossover.Projenitor1.Valor, format(crossover.Projenitor1.Valor, "b"),
                                      crossover.Projenitor2.Valor, format(crossover.Projenitor2.Valor, "b"),
                                      crossover.Hijo1.Valor, format(crossover.Hijo1.Valor, "b"),
                                      crossover.Hijo2.Valor, format(crossover.Hijo2.Valor, "b"),
                                      crossover.Unidades])
            for mutacion in poblacion.Mutaciones:
                dataMutacion.append(
                    [iteracion, mutacion.Original.Valor, format(mutacion.Original.Valor, "b"),
                     mutacion.Mutante.Valor, format(mutacion.Mutante.Valor, "b"), mutacion.IndiceBitCambiado])
            dataPromedios.append([iteracion, poblacion.Promedio(FuncionObjetivo)])
            maximo = poblacion.Maximo()
            minimo = poblacion.Minimo()
            dataMaximos.append(
                [iteracion, maximo.Valor, FuncionObjetivo(maximo.Valor), FuncionFitness(poblacion, maximo)])
            dataMinimos.append(
                [iteracion, minimo.Valor, FuncionObjetivo(minimo.Valor), FuncionFitness(poblacion, minimo)])

            iteracion += 1
        worksheetIteraciones.add_table(
            'A1:D' + str(self.Configuracion.Iteraciones * self.Configuracion.CantidadPoblacionInicial + 1),
            {'data': dataIteraciones,
             'columns': [
                 {'header': 'Iteracion'},
                 {'header': 'Valor'},
                 {'header': 'Objetivo'},
                 {'header': 'Fitness'}]})

        worksheetPromedios.add_table('A1:B' + str(self.Configuracion.Iteraciones + 1), {'data': dataPromedios,
                                                                                        'columns': [
                                                                                            {'header': 'Iteracion'},
                                                                                            {'header': 'Promedio'}]})
        chartPromedio = workbook.add_chart({'type': 'line'})
        chartPromedio.add_series(
            {'values': '=Promedios!$B$2:$B$' + str(self.Configuracion.Iteraciones + 1), 'name': 'Promedios'})
        chartPromedio.set_x_axis({'name': 'Iteraciones'})
        chartPromedio.set_y_axis({'name': 'Promedio Objetivo'})
        worksheetPromedios.insert_chart('C1', chartPromedio)

        worksheetMaximos.add_table('A1:D' + str(self.Configuracion.Iteraciones + 1), {'data': dataMaximos,
                                                                                      'columns': [
                                                                                          {'header': 'Iteracion'},
                                                                                          {'header': 'Valor'},
                                                                                          {'header': 'Objetivo'},
                                                                                          {'header': 'Fitness'}]})

        chartMaximo = workbook.add_chart({'type': 'line'})
        chartMaximo.add_series(
            {'values': '=Maximos!$C$2:$C$' + str(self.Configuracion.Iteraciones + 1), 'name': 'Maximos'})
        chartMaximo.set_x_axis({'name': 'Iteraciones'})
        chartMaximo.set_y_axis({'name': 'Objetivo'})
        worksheetMaximos.insert_chart('E1', chartMaximo)
        worksheetMinimos.add_table('A1:D' + str(self.Configuracion.Iteraciones + 1), {'data': dataMinimos,
                                                                                      'columns': [
                                                                                          {'header': 'Iteracion'},
                                                                                          {'header': 'Valor'},
                                                                                          {'header': 'Objetivo'},
                                                                                          {'header': 'Fitness'}]})
        chartMinimo = workbook.add_chart({'type': 'line'})
        chartMinimo.add_series(
            {'values': '=Minimos!$C$2:$C$' + str(self.Configuracion.Iteraciones + 1), 'name': 'Minimos'})
        chartMinimo.set_x_axis({'name': 'Iteraciones'})
        chartMinimo.set_y_axis({'name': 'Objetivo'})
        worksheetMinimos.insert_chart('E1', chartMinimo)

        worksheetConfiguracion.write(0, 0, "Probabilidad Crossover:", bold)
        worksheetConfiguracion.write_number(0, 1, self.Configuracion.ProbabilidadCrossover)
        worksheetConfiguracion.write(1, 0, "Probabilidad Mutacion:", bold)
        worksheetConfiguracion.write_number(1, 1, self.Configuracion.ProbabilidadMutacion)
        worksheetConfiguracion.write(2, 0, "Cantidad Poblacion Inicial:", bold)
        worksheetConfiguracion.write_number(2, 1, self.Configuracion.CantidadPoblacionInicial)
        worksheetConfiguracion.write(3, 0, "Iteraciones:", bold)
        worksheetConfiguracion.write_number(3, 1, self.Configuracion.Iteraciones)

        worksheetCrossovers.add_table(
            'A1:J' + str(len(dataCrosovers) + 1),
            {'data': dataCrosovers,
             'columns': [
                 {'header': 'Iteracion'},
                 {'header': 'Progenitor 1'},
                 {'header': 'Binario 1'},
                 {'header': 'Progenitor 2'},
                 {'header': 'Binario 2'},
                 {'header': 'Hijo 1'},
                 {'header': 'Binario Hijo 1'},
                 {'header': 'Hijo 2'},
                 {'header': 'Binario Hijo 2'},
                 {'header': 'Unidad De Corte'}
             ]})

        worksheetMutaciones.add_table(
            'A1:F' + str(len(dataMutacion) + 1),
            {'data': dataMutacion,
             'columns': [
                 {'header': 'Iteracion'},
                 {'header': 'Original'},
                 {'header': 'Original Binario'},
                 {'header': 'Mutante'},
                 {'header': 'Mutante Binario'},
                 {'header': 'Indice Cambiado'}
             ]})

        workbook.close()

        print(fullPath)
        os.startfile(fullPath, 'open')
