from TP_Investigacion_Fractales.AlgoritmoGenetico import AlgoritmoGenetico
from TP_Investigacion_Fractales.Configuracion import Configuracion
import matplotlib.image as mpimg
import time

from TP_Investigacion_Fractales.ImagenHelper import *


def test_ga(configuracion: Configuracion, ventana=None):
    seconds = time.time()
    algoritmo = AlgoritmoGenetico(configuracion)
    algoritmo.Run(ventana)
    mejorCromosoma = algoritmo.GetMejorCromosoma()
    img = mpimg.imread(configuracion.ImagePath)
    img = get_greyscale_image(img)
    plt.figure()
    plt.imshow(img, cmap='gray', interpolation='none')
    plt.title('Imagen Comun')
    compresion = configuracion.Destination_Size / configuracion.Source_Size
    iterations = decompress(mejorCromosoma.Transformaciones, configuracion.Source_Size,
                            configuracion.Source_Size // int(1 // (1 - compresion)), configuracion.Source_Size)
    # plot_iterations(iterations)
    plot_iterations(iterations, img)
    plt.figure()
    plt.imshow(iterations[len(iterations) - 1], cmap='gray', vmin=0, vmax=255, interpolation='none')

    lastseconds = time.time()
    print('Tardo:' + repr(lastseconds - seconds) + 'Segundos')
    plt.title('Ultima Iteracion - Tardo: ' + repr(lastseconds - seconds) + 'Segundos')
    # mpimg.imsave('dolly_Zero_fractal_.jpg', iterations[0], cmap='gray', vmin=0, vmax=255, interpolation='none')
    mpimg.imsave('dolly_Ultima_fractal_.jpg', iterations[len(iterations) - 1], cmap='gray', vmin=0, vmax=255)
    plt.show()


def decompress(transformations, source_size, destination_size, step, nb_iter=8):
    print('Recontruyendo imagen a partir de las transformaciones obtenidas')
    factor = source_size // destination_size
    height = len(transformations) * destination_size
    width = len(transformations[0]) * destination_size
    iterations = [np.random.randint(0, 256, (height, width))]
    cur_img = np.zeros((height, width))
    for i_iter in range(nb_iter):
        print('Iteracion para contruir imagen: ' + repr(i_iter) + '/' + repr(nb_iter))
        for i in range(len(transformations)):
            for j in range(len(transformations[i])):
                # Apply transform
                k = transformations[i][j].X
                l = transformations[i][j].Y
                flip = transformations[i][j].IsometricFlip[0]
                angle = transformations[i][j].IsometricFlip[1]
                contrast = transformations[i][j].Contrast
                brightness = transformations[i][j].Brightness
                S = reduce(iterations[-1][k * step:k * step + source_size, l * step:l * step + source_size], factor)
                D = apply_transformation(S, flip, angle, contrast, brightness)
                cur_img[i * destination_size:(i + 1) * destination_size,
                j * destination_size:(j + 1) * destination_size] = D
        iterations.append(cur_img)
        cur_img = np.zeros((height, width))
    return iterations
