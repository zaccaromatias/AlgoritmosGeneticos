# Importamos las funciones para obtener numeros aleatorios
from random import randint, uniform, random
# Para el manejo de la ruta de archivo
from path import Path
import os

# Para la exportacion a excel
import datetime
import xlsxwriter

from Ejercicio3.Cromosoma import Cromosoma
from Ejercicio3.Crossover import Crossover
from Ejercicio3.Mutacion import Mutacion
from Ejercicio3.Poblacion import Poblacion


# Logica del crossover
# Recive dos cromosomas que son los que va a cruzar
# Devuelve una tupla de 3 valores donde los dos primeros son los cromosomas hijos de la cruza y el tercero es un valor
# entero del punto donde se corto
# Dicho valor de corte es un entero al azar entre 0 y 30 (largo de nuestros cromosomas)
def AplicarCrosOverDeTipoUnPunto(cromosoma1: Cromosoma, cromosoma2: Cromosoma):
    unidades = randint(0, len(cromosoma1.Valor) - 1)
    primeraParteBinario1 = cromosoma1.Valor[:unidades]
    primeraParteBinario2 = cromosoma2.Valor[:unidades]
    segundaParteBinario1 = cromosoma1.Valor[unidades:]
    segundaParteBinario2 = cromosoma2.Valor[unidades:]
    nuevoBinario1 = primeraParteBinario1 + segundaParteBinario2
    nuevoBinario2 = primeraParteBinario2 + segundaParteBinario1
    return Cromosoma(nuevoBinario1), Cromosoma(nuevoBinario2), unidades


# De la lista de cromosomas que recive devuelve uno tomado al azar
# Simplemente toma un valor entero al azar y devuelve el objeto en ese indice
def SeleccionarCromosomaAlAzar(cromosomas: []) -> Cromosoma:
    numero = randint(0, len(cromosomas) - 1)
    return cromosomas[numero]


# Logica de la mutacion
# Recive un objeto poblacion al cual agregara la mutacion y un Cromosoma el cual es el que va a mutar
# Simplemente elige un numero entero al azar entre 0 y 30 e invierte el valor de dicho valor en ese indice
def AplicarMutacion(poblacion: Poblacion, cromosoma: Cromosoma):
    mutacion = Mutacion(cromosoma)
    numeroBit = randint(0, len(cromosoma.Valor) - 1)
    list1 = list(cromosoma.Valor)
    if list1[numeroBit] == '0':
        list1[numeroBit] = '1'
    else:
        list1[numeroBit] = '0'
    mutacion.Mutante.Valor = ''.join(list1)
    mutacion.IndiceBitCambiado = numeroBit
    cromosoma.Valor = ''.join(list1)
    poblacion.Mutaciones.append(mutacion)


# Esta es nuestra funcion objetivo dada por el enunciado
# int(c.Valor,2) convierte nuestro string binario a un numero entero
def FuncionObjetivo(c: Cromosoma):
    return pow(int(c.Valor, 2) / (pow(2, 30) - 1), 2)


# Forma de calcular el fitness de cada cromosoma
# Funcion objetiva de dicho cromosoma sobre la suma la funcion objetivo de cada cromosoma de la poblacion
def FuncionFitness(poblacionInicial: Poblacion, cromosoma: Cromosoma):
    return FuncionObjetivo(cromosoma) / sum(
        FuncionObjetivo(cr) for cr in poblacionInicial.Cromosomas)


# Clase principal de nuestro programa
class AlgoritmoGenetico:
    # Cantidad de genes empleado para la creacion de la poblacion inicial
    dominioFinal = 30

    # Iniciacion de variables, recive el objeto configuracion que contiene la paremetrizacion de nuestro programa
    def __init__(self, configuracion):
        self.Configuracion = configuracion
        self.Poblaciones = []
        self.PoblacionActual = []

    # Metodo principal que realiza las iteraciones del programa
    def Run(self):
        for i in range(self.Configuracion.Iteraciones):
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
            # Variante para una mayor diversidad genetica - agregado extra solo para comparar resultados
            if self.Configuracion.DiversidadGenetica:
                self.DiversidadGenetica(nuevaPoblacion)
            nuevaPoblacion = self.Seleccionar(nuevaPoblacion)
            nuevaPoblacion = self.EvaluarCrossover(nuevaPoblacion)
            self.EvaluarMutacion(nuevaPoblacion)
            self.Poblaciones.append(nuevaPoblacion)

    # Genera la poblacion inicial generando cromosomas con valores binarios totalmente aleatorios
    def GetPoblacionInicial(self) -> Poblacion:
        poblacion = Poblacion()
        for i in range(self.Configuracion.CantidadPoblacionInicial):
            numeroRandom = ""
            for j in range(self.dominioFinal):
                numeroRandom += str(randint(0, 1))
            poblacion.Cromosomas.append(Cromosoma(numeroRandom))
        return poblacion

    # Metodo extra para generar una mayor diversidad genetica
    def DiversidadGenetica(self, poblacionInicial: Poblacion):
        similares = list(filter(lambda c: 0.105 >= FuncionFitness(poblacionInicial, c) > 0.09,
                                poblacionInicial.Cromosomas))
        if len(similares) >= 6:
            for cr in similares:
                if random() < 0.4 and not cr.EsElite:
                    numeroBit = randint(0, len(cr.Valor) - 1)
                    list1 = list(cr.Valor)
                    if list1[numeroBit] == '0':
                        list1[numeroBit] = '1'
                    else:
                        list1[numeroBit] = '0'
                    cr.Valor = ''.join(list1)

    # Llama a aplicar seleccion ruleta
    def Seleccionar(self, poblacionInicial: Poblacion) -> Poblacion:
        return self.AplicarSeleccionRuedadeRuleta(poblacionInicial)

    # Logica de seleccion de cromosomas a traves del metodo de la ruleta
    # Segun el fitnes de cada cromosomas le seteamos los valores Minimos y maximos de la porcion que ocuparian
    # (entre 0 y 1) acumulamos
    # Seleccionamos un numero decimal aleatorio entre 0 y 1 y verificamos a que cromosoma corresponde segun su porcion
    # Asi hasta completar poblacion
    def AplicarSeleccionRuedadeRuleta(self, poblacionInicial: Poblacion) -> Poblacion:
        porciones = []
        nuevaPoblacion = Poblacion()

        elite = list(filter(lambda c: c.EsElite == True, poblacionInicial.Cromosomas))
        for cromosomaElite in elite:
            nuevaPoblacion.Cromosomas.append(cromosomaElite.Clone())

        for cromosoma in poblacionInicial.Cromosomas:
            if len(porciones) == 0:
                valorMinimo = 0
            else:
                valorMinimo = porciones[len(porciones) - 1].ValorMaximo
            valorMaximo = valorMinimo + FuncionFitness(poblacionInicial, cromosoma)
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

    # Logica para marcar los mejores 2 cromosomas segun su fitnes
    # Recorre dos veces buscando el mayor fitnes entre los Cromosomas  que no son elites
    # Luego el cromosoma correspondiente para marcarlo como elite
    def Elite(self, poblacionInicial: Poblacion) -> Poblacion:
        countTrue = 0
        while countTrue < 2:
            elite = 0
            noElite = list(filter(lambda cd: cd.EsElite == False, poblacionInicial.Cromosomas))
            for cromosoma in noElite:
                if FuncionFitness(poblacionInicial, cromosoma) > elite:
                    elite = FuncionFitness(poblacionInicial, cromosoma)
            for cromosoma in noElite:
                if FuncionFitness(poblacionInicial, cromosoma) == elite and countTrue < 2:
                    Cromosoma.Elite(cromosoma)
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
        elite = list(filter(lambda c: c.EsElite == True, poblacionInicial.Cromosomas))
        for i in elite:
            nuevaPoblacion.Cromosomas.append(i.Clone())
        while len(nuevaPoblacion.Cromosomas) < self.Configuracion.CantidadPoblacionInicial:
            cromosoma1: Cromosoma = SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas).Clone()
            cromosoma2: Cromosoma = SeleccionarCromosomaAlAzar(poblacionInicial.Cromosomas).Clone()
            if self.AplicaCrossover():
                hijos = AplicarCrosOverDeTipoUnPunto(cromosoma1, cromosoma2)
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
        cromosomasNoElites = list(filter(lambda c: c.EsElite == False, poblacionInicial.Cromosomas))
        for cromosoma in cromosomasNoElites:
            if self.AplicaMutacion():
                AplicarMutacion(poblacionInicial, cromosoma)

    # Muestra en pantalla los resultados de las iteraciones y el maximo obtenido
    def Print(self):
        # self.PrintIteraciones()
        self.PrintMaximo()

    # Muestra en pantalla el maximo de todas las poblaciones
    def PrintMaximo(self):
        print("******* Maximo Calculado: ")
        maximo = self.GetMaximoTotal()
        print("- Iteracion: " + str(maximo[0]) + "- Objetivo: " + str(
            FuncionObjetivo(maximo[1])) + "- Cromosoma: " + maximo[1].Valor)

    # Devuelve el cromosoma con el valor objetivo maximo obtenido
    def GetMaximoTotal(self):
        maximos = []
        iteracion = 1
        for poblacion in self.Poblaciones:
            maximos.append([iteracion, poblacion.Maximo(FuncionObjetivo)])
            iteracion += 1
        valorMaximo = max(FuncionObjetivo(cromosoma[1]) for cromosoma in maximos)
        maximo = list(filter(lambda c: FuncionObjetivo(c[1]) == valorMaximo, maximos))[0]
        return maximo

    # Muestra en pantalla valores de las iteraciones
    def PrintIteraciones(self):
        iteracion = 1
        for poblacion in self.Poblaciones:
            print("*******Poblacion Numero: " + str(iteracion))
            poblacion.Print(FuncionObjetivo, FuncionFitness)
            iteracion = iteracion + 1

    # ----------------------------------------------------------------------------------------------------------------------

    # Exporta a excel los resultados, iteraciones, maximos, minimos, promedios junto a la grafica
    def ExportToExcel(self):
        iteracion = 1
        dataResultados = []
        dataIteraciones = []
        dataCrosovers = []
        dataMutacion = []
        # Carga las diferentes listas con los correspondiente valores
        for poblacion in self.Poblaciones:
            self.CargarDatosDeIteraciones(dataIteraciones, iteracion, poblacion)
            self.CargarDatosCrossovers(dataCrosovers, iteracion, poblacion)
            self.CargarDatosMutaciones(dataMutacion, iteracion, poblacion)
            self.CargarDatosResultados(dataResultados, iteracion, poblacion)
            iteracion += 1
        # Genera un archivo xlsx con la siguiente nomenclatura YYYY-mm-dd-HH-MM-S.xlsx y lo genera dentro de la carpeta Excels
        name = str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")) + '.xlsx'
        pathExcels = "Excels/" + name
        workbook = xlsxwriter.Workbook(pathExcels)
        bold = workbook.add_format({'bold': 1})
        #Genera los sheet con cada uno de los datos
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
        worksheetMutaciones.write('C1', 'Mutante', bold)
        worksheetMutaciones.write('D1', 'Indice Cambiado', bold)
        worksheetMutaciones.add_table(
            'A1:D' + str(len(dataMutacion) + 1),
            {'data': dataMutacion,
             'columns': [
                 {'header': 'Iteracion'},
                 {'header': 'Original'},
                 {'header': 'Mutante'},
                 {'header': 'Indice Cambiado'}
             ]})

    def CargarSheetCrossovers(self, workbook, dataCrosovers, bold):
        worksheetCrossovers = workbook.add_worksheet("Crossovers")
        worksheetCrossovers.write('A1', 'Iteracion', bold)
        worksheetCrossovers.write('B1', 'Progenitor 1', bold)
        worksheetCrossovers.write('C1', 'Progenitor 2', bold)
        worksheetCrossovers.write('D1', 'Hijo 1', bold)
        worksheetCrossovers.write('E1', 'Hijo 2', bold)
        worksheetCrossovers.write('F1', 'Unidad Corte', bold)
        worksheetCrossovers.add_table(
            'A1:F' + str(len(dataCrosovers) + 1),
            {'data': dataCrosovers,
             'columns': [
                 {'header': 'Iteracion'},
                 {'header': 'Progenitor 1'},
                 {'header': 'Progenitor 2'},
                 {'header': 'Hijo 1'},
                 {'header': 'Hijo 2'},
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
        worksheetConfiguracion.write(4, 0, "Elitismo:", bold)
        worksheetConfiguracion.write(4, 1, str(self.Configuracion.Elite))

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
                                                                                                 'header': 'Cromosoma(Maximo)'},
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
        worksheetIteraciones.write('E1', 'Elite', bold)
        worksheetIteraciones.add_table(
            'A1:E' + str(self.Configuracion.Iteraciones * self.Configuracion.CantidadPoblacionInicial + 1),
            {'data': dataIteraciones,
             'columns': [
                 {'header': 'Iteracion'},
                 {'header': 'Valor'},
                 {'header': 'Objetivo'},
                 {'header': 'Fitness'},
                 {'header': 'Elite'}]})

    def CargarDatosResultados(self, dataResultados, iteracion, poblacion):
        maximo = poblacion.Maximo(FuncionObjetivo)
        minimo = poblacion.Minimo(FuncionObjetivo)
        dataResultados.append(
            [iteracion, FuncionObjetivo(minimo), FuncionObjetivo(maximo), maximo.Valor,
             poblacion.Promedio(FuncionObjetivo)])

    def CargarDatosMutaciones(self, dataMutacion, iteracion, poblacion):
        for mutacion in poblacion.Mutaciones:
            dataMutacion.append(
                [iteracion, mutacion.Original.Valor,
                 mutacion.Mutante.Valor, mutacion.IndiceBitCambiado])

    def CargarDatosCrossovers(self, dataCrosovers, iteracion, poblacion):
        for crossover in poblacion.Crossovers:
            dataCrosovers.append([iteracion, crossover.Projenitor1.Valor,
                                  crossover.Projenitor2.Valor,
                                  crossover.Hijo1.Valor,
                                  crossover.Hijo2.Valor,
                                  crossover.Unidades])

    def CargarDatosDeIteraciones(self, dataIteraciones, iteracion, poblacion):
        for cromosoma in poblacion.Cromosomas:
            elite = "Sí"
            if not cromosoma.EsElite:
                elite = "No"
            fila = [iteracion, cromosoma.Valor, FuncionObjetivo(cromosoma),
                    FuncionFitness(poblacion, cromosoma), elite]
            dataIteraciones.append(fila)
