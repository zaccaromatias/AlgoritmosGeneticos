# Archivo al que llamamos para iniciar nuestro código
# Simplemente crea una instancia de Program y llama al método Run() del mismo.
# Si se desea interactuar con una interfaz gráfica, se puede prescindir de Program.py y utilizar AlgoritmoGeneticoView.py
from Ejercicio3.DistanciaHelper import DistanciaHelper
from Ejercicio3.Program import Program
from Ejercicio3.ProgramView import ProgramView

DistanciaHelper.LoadTablaDistanciaYCapitales()
DistanciaHelper.GetAllCiudades()
# Program().Run()
ProgramView().Show()
