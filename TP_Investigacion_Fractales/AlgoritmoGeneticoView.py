from tkinter import *
from tkinter import ttk

from TP_Investigacion_Fractales.CompresionAlgoritmoGenetico import test_ga
from TP_Investigacion_Fractales.Configuracion import ConfigurationViewModel


class AlgoritmoGeneticoView(Toplevel):

    # Se definen las características de la ventana principal.
    def __init__(self, configurationViewModel: ConfigurationViewModel, master=None):
        super().__init__(master=master)
        self.title("Configuracion de Algoritmos Genéticos")

        self.geometry("370x250")
        self.resizable(False, False)
        self.ConfigurationViewModel = configurationViewModel

        lblProbabilidadCrossover = Label(self, text="Probabilidad de crossover (entre 0 y 1): ")
        txtProbabilidadCrossover = Spinbox(self,
                                           from_=0, to=1, increment=0.05,
                                           textvariable=self.ConfigurationViewModel.ProbabilidadCrossover)

        lblProbabilidadMutacion = Label(self, text="Probabilidad de mutación (entre 0 y 1): ")
        txtProbabilidadMutacion = Spinbox(self, from_=0, to=1, increment=0.05,
                                          textvariable=self.ConfigurationViewModel.ProbabilidadMutacion)

        lblTamanioPoblacion = Label(self, text="Tamaño de población: ")
        txtTamanioPoblacion = Entry(self, textvariable=self.ConfigurationViewModel.NumeroCromosomasPoblacion)

        lblCantidadIteraciones = Label(self, text="Cantidad de iteraciones: ")
        txtCantidadIteraciones = Entry(self, textvariable=self.ConfigurationViewModel.Iteraciones)

        lblelitismo = Label(self, text="Elitismo")
        chkElitismo = Checkbutton(self, variable=self.ConfigurationViewModel.Elite, onvalue=True, offvalue=False)

        btnrun = Button(self, text="Ejecutar", command=lambda: self.Run())

        lblCantidadDeElites = Label(self, text="Cantidad de Elites: ")
        txtCantidadElites = Spinbox(self, from_=1, to=9999999, increment=1,
                                    textvariable=self.ConfigurationViewModel.CantidadElites)
        self.progress = ttk.Progressbar(self, orient=HORIZONTAL,
                                        length=200, mode='determinate')

        # Se ubican los diferentes elementos de la ventana dentro de ella.
        lblProbabilidadCrossover.pack()
        lblProbabilidadCrossover.place(x=10, y=10)
        txtProbabilidadCrossover.pack()
        txtProbabilidadCrossover.place(x=230, y=10)
        lblProbabilidadMutacion.pack()
        lblProbabilidadMutacion.place(x=10, y=40)
        txtProbabilidadMutacion.pack()
        txtProbabilidadMutacion.place(x=230, y=40)
        lblTamanioPoblacion.pack()
        lblTamanioPoblacion.place(x=10, y=70)
        txtTamanioPoblacion.pack()
        txtTamanioPoblacion.place(x=230, y=70)
        lblCantidadIteraciones.pack()
        lblCantidadIteraciones.place(x=10, y=100)
        txtCantidadIteraciones.pack()
        txtCantidadIteraciones.place(x=230, y=100)
        lblCantidadDeElites.pack()
        lblCantidadDeElites.place(x=10, y=130)
        txtCantidadElites.pack()
        txtCantidadElites.place(x=230, y=130)
        lblelitismo.pack()
        lblelitismo.place(x=10, y=160)
        chkElitismo.pack()
        chkElitismo.place(x=230, y=160)

        btnrun.pack()
        btnrun.place(x=240, y=220)
        self.progress.pack()
        self.progress.place(x=10, y=220)

    # Este método se invoca al hacer click en Ejecutar y se encarga de invocar a los métodos del algoritmo proveyendo
    # los parámetros ingresados.
    def Run(self):
        self.progress['value'] = 0
        self.update_idletasks()
        config = self.ConfigurationViewModel.ToConfiguration()
        test_ga(config, self)
        self.progress['value'] = 0
        self.update_idletasks()
