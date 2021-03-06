from Ejercicio3.Capital import Capital
from Ejercicio3.DistanciaHelper import DistanciaHelper


class Heuristica:

    @staticmethod
    def CalcularRecorridoIniciandoEn(ciudadPartida: Capital, ventana=None) -> []:
        recorrido = []
        DistanciaHelper.ResetVisitadas()  # Saca el tilde de visitadas
        ciudadActual = ciudadPartida
        while ciudadActual is not None:
            if ventana is not None:
                ventana.progress['value'] += (100 / len(DistanciaHelper.Capitales))
                ventana.update_idletasks()
            recorrido.append(ciudadActual)
            ciudadActual.SetVisitada(True)
            ciudadActual = Heuristica.BuscarCiudadMasCercana(ciudadActual)
        # Para volver a la ciudad origen
        recorrido.append(recorrido[0])
        return recorrido

    @staticmethod
    def BuscarCiudadMasCercana(actual: Capital) -> Capital:
        """Busca la ciudad mas cercana a la actual de las que no se visitaron"""
        destino = None
        minimaDistancia = None
        for posibleDestino in list(
                filter(lambda capital: capital.Visitada is False and capital != actual, DistanciaHelper.Capitales)):
            distancia = DistanciaHelper.GetDistancia(actual, posibleDestino)
            if (minimaDistancia is None or distancia < minimaDistancia):
                minimaDistancia = distancia
                destino = posibleDestino
        return destino

    @staticmethod
    def CalcularMejorRecorrido(ventana=None) -> []:
        mejorRecorrido = None
        minimaDistancia = None
        for capital in DistanciaHelper.Capitales:
            if ventana is not None:
                ventana.progress['value'] += (100 / len(DistanciaHelper.Capitales))
                ventana.update_idletasks()
            recorrido = Heuristica.CalcularRecorridoIniciandoEn(capital)
            distancia = DistanciaHelper.GetDistanciaTotal(recorrido)
            if minimaDistancia is None or distancia < minimaDistancia:
                mejorRecorrido = recorrido
                minimaDistancia = distancia
        return mejorRecorrido
