import matplotlib.pyplot as plt
from itertools import islice
from openpyxl import load_workbook
from pandas import DataFrame

# Esto es un ejemplo de prueba no mas. REFACTORIZAR
# Leee el valor de las coordenadas de la segunda hoja del excel
# Y agrega todos los puntos  uniendolo con el anteior

wb = load_workbook(filename='TablaCapitales.xlsx')
ws = wb['Coordenadas']
data = ws.values
cols = next(data)[1:]
data = list(data)
idx = [r[0] for r in data]
data = (islice(r, 1, None) for r in data)
df = DataFrame(data, index=idx, columns=cols)

indice = 0
anterior = None
for value in df.iterrows():
    plt.scatter(value[1].Lat, value[1].Long, s=100)
    plt.annotate(value[0], (value[1].Lat, value[1].Long))
    if (anterior != None):
        x_values = [anterior[0], value[1].Lat]
        y_values = [anterior[1], value[1].Long]
        plt.plot(x_values, y_values)
        anterior = [value[1].Lat, value[1].Long]
    else:
        anterior = [value[1].Lat, value[1].Long]
    indice += 1
plt.show()
