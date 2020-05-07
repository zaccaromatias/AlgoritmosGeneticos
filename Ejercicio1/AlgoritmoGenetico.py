from random import randint, uniform, random
from path import Path

import datetime
import os
import xlsxwriter

from Ejercicio1.Cromosoma import Cromosoma
from Ejercicio1.Crossover import Crossover
from Ejercicio1.Mutacion import Mutacion
from Ejercicio1.Poblacion import Poblacion


def AplicarCrosOverDeTipoUnPunto(cromosoma1: Cromosoma, cromosoma2: Cromosoma):
    unidades = randint(0, len(cromosoma1.Valor) - 1)
    primeraParteBinario1 = cromosoma1.Valor[:unidades]
    primeraParteBinario2 = cromosoma2.Valor[:unidades]
    segundaParteBinario1 = cromosoma1.Valor[unidades:]
    segundaParteBinario2 = cromosoma2.Valor[unidades:]
    nuevoBinario1 = primeraParteBinario1 + segundaParteBinario2
    nuevoBinario2 = primeraParteBinario2 + segundaParteBinario1
    return Cromosoma(nuevoBinario1), Cromosoma(nuevoBinario2), unidades


def SeleccionarCromosomaAlAzar(cromosomas: []) -> Cromosoma:
    numero = randint(0, len(cromosomas) - 1)
    return cromosomas[numero]


def AplicarMutacion(poblacion: Poblacion, cromosoma: Cromosoma):
    mutacion = Mutacion(cromosoma.Clone())
    numeroBit = randint(0, len(mutacion.Original.Valor) - 1)
    list1 = list(mutacion.Mutante.Valor)
    if mutacion.Mutante.Valor[numeroBit] == '0':
        list1[numeroBit] = '1'
    else:
        list1[numeroBit] = '0'
    mutacion.Mutante.Valor = ''.join(list1)
    mutacion.IndiceBitCambiado = numeroBit
    poblacion.Mutaciones.append(mutacion)


def FuncionObjetivo(c: Cromosoma):
    return pow(int(c.Valor, 2) / (pow(2, 30) - 1), 2)


def FuncionFitness(poblacionInicial: Poblacion, cromosoma: Cromosoma):
    return FuncionObjetivo(cromosoma) / sum(
        FuncionObjetivo(cr) for cr in poblacionInicial.Cromosomas)


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
            nuevaPoblacion: Poblacion = self.PoblacionActual
            if self.Configuracion.Elite:
                nuevaPoblacion = self.Elite(nuevaPoblacion)
            nuevaPoblacion = self.Seleccionar(nuevaPoblacion)
            nuevaPoblacion = self.EvaluarCrossover(nuevaPoblacion)
            self.EvaluarMutacion(nuevaPoblacion)
            self.Poblaciones.append(nuevaPoblacion)

    def GetPoblacionInicial(self) -> Poblacion:
        poblacion = Poblacion()
        for i in range(self.Configuracion.CantidadPoblacionInicial):
            numeroRandom = ""
            for j in range(self.dominioFinal):
                numeroRandom += str(randint(0, 1))
            poblacion.Cromosomas.append(Cromosoma(numeroRandom))
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

        elite = list(filter(lambda c: c.Elite == True, poblacionInicial.Cromosomas))
        nuevaPoblacion.Cromosomas.extend(elite)
        for i in range(self.Configuracion.CantidadPoblacionInicial - len(elite)):
            numero = random()
            lista = list(filter(
                lambda c: c.PorcionRuleta.ValorMinimo <= numero <= c.PorcionRuleta.ValorMaximo,
                poblacionInicial.Cromosomas))
            cromosomaSeleccionado = Cromosoma.Clone(lista[0])
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
        elite = list(filter(lambda c: c.Elite == True, poblacionInicial.Cromosomas))
        for i in elite:
            nuevaPoblacion.Cromosomas.append(i)
        while len(nuevaPoblacion.Cromosomas) < self.Configuracion.CantidadPoblacionInicial:
            cromosoma1: Cromosoma = Cromosoma.Clone(SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas))
            cromosoma2: Cromosoma = Cromosoma.Clone(SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas))
            if self.AplicaCrossover():
                hijos = AplicarCrosOverDeTipoUnPunto(cromosoma1, cromosoma2)
                nuevaPoblacion.Cromosomas.append(hijos[0])
                nuevaPoblacion.Cromosomas.append(hijos[1])
                nuevaPoblacion.Crossovers.append(Crossover(cromosoma1, cromosoma2, hijos[0], hijos[1], hijos[2]))
            else:
                nuevaPoblacion.Cromosomas.append(cromosoma1.Clone())
                nuevaPoblacion.Cromosomas.append(cromosoma2.Clone())
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
        self.PrintIteraciones()
        self.PrintMaximo()

    def PrintMaximo(self):
        print("******* Maximo Calculado: ")
        maximo = self.GetMaximoTotal()
        print("- Iteracion: " + str(maximo[0]) + "- Objetivo: " + str(
            FuncionObjetivo(maximo[1])) + "- Cromosoma: " + maximo[1].Valor)

    def GetMaximoTotal(self):
        maximos = []
        iteracion = 1
        for poblacion in self.Poblaciones:
            maximos.append([iteracion, poblacion.Maximo(FuncionObjetivo)])
            iteracion += 1
        valorMaximo = max(FuncionObjetivo(cromosoma[1]) for cromosoma in maximos)
        maximo = list(filter(lambda c: FuncionObjetivo(c[1]) == valorMaximo, maximos))[0]
        return maximo

    def PrintIteraciones(self):
        iteracion = 1
        for poblacion in self.Poblaciones:
            print("*******Poblacion Numero: " + str(iteracion))
            poblacion.Print(FuncionObjetivo, FuncionFitness)
            iteracion = iteracion + 1

    # ----------------------------------------------------------------------------------------------------------------------

    def ExportToExcel(self):
        iteracion = 1
        dataResultados = []
        dataIteraciones = []
        dataCrosovers = []
        dataMutacion = []
        for poblacion in self.Poblaciones:
            self.CargarDatosDeIteraciones(dataIteraciones, iteracion, poblacion)
            self.CargarDatosCrossovers(dataCrosovers, iteracion, poblacion)
            self.CargarDatosMutaciones(dataMutacion, iteracion, poblacion)
            self.CargarDatosResultados(dataResultados, iteracion, poblacion)
            iteracion += 1
        name = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.xlsx'
        pathExcels = "Excels/" + name
        workbook = xlsxwriter.Workbook(pathExcels)
        bold = workbook.add_format({'bold': 1})
        self.CargarSheetDeResultados(workbook, dataResultados, bold)
        self.CargarSheetDeIteraciones(workbook, dataIteraciones, bold)
        self.CargarSheetCrossovers(workbook, dataCrosovers, bold)
        self.CargarSheetMutaciones(workbook, dataMutacion, bold)
        self.CargarSheetConfiguracion(workbook, bold)
        workbook.close()
        fullPath = Path(pathExcels).abspath()
        os.startfile(fullPath, 'open')

    def CargarSheetMutaciones(self, workbook, dataMutacion, bold):
        worksheetMutaciones = workbook.add_worksheet("Mutaciones")
        worksheetMutaciones.write('A1', 'Iteracion', bold)
        worksheetMutaciones.write('B1', 'Original', bold)
        worksheetMutaciones.write('C1', 'Original Binario', bold)
        worksheetMutaciones.write('D1', 'Mutante', bold)
        worksheetMutaciones.write('E1', 'Mutante Binario', bold)
        worksheetMutaciones.write('F1', 'Indice Cambiado', bold)
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

    def CargarSheetCrossovers(self, workbook, dataCrosovers, bold):
        worksheetCrossovers = workbook.add_worksheet("Crossovers")
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

    def CargarSheetConfiguracion(self, workbook, bold):
        worksheetConfiguracion = workbook.add_worksheet("Configuracion")
        worksheetConfiguracion.write(0, 0, "Probabilidad Crossover:", bold)
        worksheetConfiguracion.write_number(0, 1, self.Configuracion.ProbabilidadCrossover)
        worksheetConfiguracion.write(1, 0, "Probabilidad Mutacion:", bold)
        worksheetConfiguracion.write_number(1, 1, self.Configuracion.ProbabilidadMutacion)
        worksheetConfiguracion.write(2, 0, "Cantidad Poblacion Inicial:", bold)
        worksheetConfiguracion.write_number(2, 1, self.Configuracion.CantidadPoblacionInicial)
        worksheetConfiguracion.write(3, 0, "Iteraciones:", bold)
        worksheetConfiguracion.write_number(3, 1, self.Configuracion.Iteraciones)

    def CargarSheetDeResultados(self, workbook, dataResultados, bold):
        worksheetResultados = workbook.add_worksheet("Resultados")
        worksheetResultados.write('A1', 'Nro Ciclo.', bold)
        worksheetResultados.write('B1', 'Minimo', bold)
        worksheetResultados.write('C1', 'Maximo', bold)
        worksheetResultados.write('D1', 'Valor Cromosoma(Maximo)', bold)
        worksheetResultados.write('E1', 'Promedio', bold)
        worksheetResultados.add_table('A1:E' + str(self.Configuracion.Iteraciones + 1), {'data': dataResultados,
                                                                                         'columns': [
                                                                                             {
                                                                                                 'header': 'Nro De Ciclo.'},
                                                                                             {'header': 'Minimo'},
                                                                                             {'header': 'Maximo'},
                                                                                             {
                                                                                                 'header': 'Crmosoma(Maximo)'},
                                                                                             {'header': 'Promedio'}
                                                                                         ]})
        maximo = self.GetMaximoTotal()
        textoMaximo = "- Iteracion: " + str(maximo[0]) + "- Objetivo: " + str(
            FuncionObjetivo(maximo[1])) + "- Cromosoma: " + maximo[1].Valor
        worksheetResultados.write('F1', 'MAXIMO:', bold)
        worksheetResultados.write('F2', textoMaximo, bold)
        chartResultados = workbook.add_chart({'type': 'line'})
        chartResultados.add_series(
            {'values': '=Resultados!$B$2:$B$' + str(self.Configuracion.Iteraciones + 1), 'name': 'Minimo'})
        chartResultados.add_series(
            {'values': '=Resultados!$C$2:$C$' + str(self.Configuracion.Iteraciones + 1), 'name': 'Maximo'})
        chartResultados.add_series(
            {'values': '=Resultados!$E$2:$E$' + str(self.Configuracion.Iteraciones + 1), 'name': 'Promedio'})

        chartResultados.set_x_axis({'name': 'Iteraciones'})
        chartResultados.set_y_axis({'name': 'Valor'})
        worksheetResultados.insert_chart('F3', chartResultados)

    def CargarSheetDeIteraciones(self, workbook, dataIteraciones, bold):
        worksheetIteraciones = workbook.add_worksheet("Iteraciones")
        worksheetIteraciones.write('A1', 'Iteracion', bold)
        worksheetIteraciones.write('B1', 'Valor', bold)
        worksheetIteraciones.write('C1', 'Objetivo', bold)
        worksheetIteraciones.write('D1', 'Fitness', bold)
        worksheetIteraciones.add_table(
            'A1:D' + str(self.Configuracion.Iteraciones * self.Configuracion.CantidadPoblacionInicial + 1),
            {'data': dataIteraciones,
             'columns': [
                 {'header': 'Iteracion'},
                 {'header': 'Valor'},
                 {'header': 'Objetivo'},
                 {'header': 'Fitness'}]})

    def CargarDatosResultados(self, dataResultados, iteracion, poblacion):
        maximo = poblacion.Maximo(FuncionObjetivo)
        minimo = poblacion.Minimo(FuncionObjetivo)
        dataResultados.append(
            [iteracion, FuncionObjetivo(minimo), FuncionObjetivo(maximo), maximo.Valor,
             poblacion.Promedio(FuncionObjetivo)])

    def CargarDatosMutaciones(self, dataMutacion, iteracion, poblacion):
        for mutacion in poblacion.Mutaciones:
            dataMutacion.append(
                [iteracion, int(mutacion.Original.Valor), mutacion.Original.Valor,
                 int(mutacion.Mutante.Valor), mutacion.Mutante.Valor, mutacion.IndiceBitCambiado])

    def CargarDatosCrossovers(self, dataCrosovers, iteracion, poblacion):
        for crossover in poblacion.Crossovers:
            dataCrosovers.append([iteracion, int(crossover.Projenitor1.Valor, 2), crossover.Projenitor1.Valor,
                                  int(crossover.Projenitor2.Valor), crossover.Projenitor2.Valor,
                                  int(crossover.Hijo1.Valor), crossover.Hijo1.Valor,
                                  int(crossover.Hijo2.Valor), crossover.Hijo2.Valor,
                                  crossover.Unidades])

    def CargarDatosDeIteraciones(self, dataIteraciones, iteracion, poblacion):
        for cromosoma in poblacion.Cromosomas:
            fila = [iteracion, cromosoma.Valor, FuncionObjetivo(cromosoma),
                    FuncionFitness(poblacion, cromosoma)]
            dataIteraciones.append(fila)
