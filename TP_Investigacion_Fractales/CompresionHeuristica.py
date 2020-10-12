import matplotlib.image as mpimg
import time
import os

from TP_Investigacion_Fractales.Configuracion import Configuracion
from TP_Investigacion_Fractales.ImagenHelper import *


def compress(img, source_size, destination_size, step):
    """Por cada bloque destino, se optimizan el brillo y contraste, se comparan todos los bloques transformados
       y se guarda el mejor. Retorna la lista de mejores transformaciones"""
    transformations = []
    transformed_blocks = generate_all_transformed_blocks(img, source_size, destination_size, step)
    i_count = img.shape[0] // destination_size
    j_count = img.shape[1] // destination_size
    for i in range(i_count):
        transformations.append([])
        for j in range(j_count):
            print("{}/{} ; {}/{}".format(i, i_count, j, j_count))
            transformations[i].append(None)
            min_d = float('inf')
            # Extract the destination block
            D = img[i * destination_size:(i + 1) * destination_size, j * destination_size:(j + 1) * destination_size]
            # Test all possible transformations and take the best one
            for k, l, direction, angle, S in transformed_blocks:
                contrast, brightness = find_contrast_and_brightness2(D, S)
                S = contrast * S + brightness
                d = np.sum(np.square(D - S))
                if d < min_d:
                    min_d = d
                    transformations[i][j] = (k, l, direction, angle, contrast, brightness)
    return transformations


def decompress(transformations, source_size, destination_size, step, nb_iter=8):
    """???"""
    factor = source_size // destination_size
    height = len(transformations) * destination_size
    width = len(transformations[0]) * destination_size
    iterations = [np.random.randint(0, 256, (height, width))]
    cur_img = np.zeros((height, width))
    for i_iter in range(nb_iter):
        print(i_iter)
        for i in range(len(transformations)):
            for j in range(len(transformations[i])):
                # Apply transform
                k, l, flip, angle, contrast, brightness = transformations[i][j]
                S = reduce(iterations[-1][k * step:k * step + source_size, l * step:l * step + source_size], factor)
                D = apply_transformation(S, flip, angle, contrast, brightness)
                cur_img[i * destination_size:(i + 1) * destination_size,
                j * destination_size:(j + 1) * destination_size] = D
        iterations.append(cur_img)
        cur_img = np.zeros((height, width))
    return iterations


# ----------------------------------------------------------------------------------------------------------------------
#                                                   RGB (HEURÍSTICA)
# ----------------------------------------------------------------------------------------------------------------------


def extract_rgb(img):
    return img[:, :, 0], img[:, :, 1], img[:, :, 2]


def assemble_rgb(img_r, img_g, img_b):
    shape = (img_r.shape[0], img_r.shape[1], 1)
    return np.concatenate((np.reshape(img_r, shape), np.reshape(img_g, shape),
                           np.reshape(img_b, shape)), axis=2)


def reduce_rgb(img, factor):
    """Reduce el tamaño de la imagen aproximando bloques lindantes aplicando reduce(factor)
       a cada color primario extraido de la imagen y volviendolos a fusionar."""
    img_r, img_g, img_b = extract_rgb(img)
    img_r = reduce(img_r, factor)
    img_g = reduce(img_g, factor)
    img_b = reduce(img_b, factor)
    return assemble_rgb(img_r, img_g, img_b)


def compress_rgb(img, source_size, destination_size, step):
    """Se aplica compress() a cada color primario extraido de la imagen y se los vuelve a fusionar."""
    img_r, img_g, img_b = extract_rgb(img)
    return [compress(img_r, source_size, destination_size, step),
            compress(img_g, source_size, destination_size, step),
            compress(img_b, source_size, destination_size, step)]


def decompress_rgb(transformations, source_size, destination_size, step, nb_iter=8):
    """Se aplica decompress() a cada color primario extraido de la imagen y se los vuelve a fusionar."""
    img_r = decompress(transformations[0], source_size, destination_size, step, nb_iter)[-1]
    img_g = decompress(transformations[1], source_size, destination_size, step, nb_iter)[-1]
    img_b = decompress(transformations[2], source_size, destination_size, step, nb_iter)[-1]
    return assemble_rgb(img_r, img_g, img_b)


def test_greyscale(configuracion: Configuracion):
    seconds = time.time()
    img = mpimg.imread(configuracion.ImagePath)
    img = get_greyscale_image(img)
    # img = reduce(img, configuracion.Destination_Size)
    plt.figure()
    plt.imshow(img, cmap='gray', interpolation='none')
    transformations = compress(img, configuracion.Source_Size, configuracion.Destination_Size, configuracion.Step)
    iterations = decompress(transformations, configuracion.Source_Size, configuracion.Destination_Size,
                            configuracion.Step)
    plot_iterations(iterations, img)
    plt.figure()
    plt.imshow(iterations[len(iterations) - 1], cmap='gray', vmin=0, vmax=255, interpolation='none')
    lastseconds = time.time()
    print('Tardo:' + repr(lastseconds - seconds) + 'Segundos')
    plt.title('Ultima Iteracion - Tardo: ' + repr(lastseconds - seconds) + 'Segundos')
    extension = os.path.splitext(configuracion.ImagePath)[-1]
    mpimg.imsave('Resultado_Heuristico' + extension, iterations[len(iterations) - 1], cmap='gray', vmin=0, vmax=255)
    plt.show()


def test_rgb():
    img = mpimg.imread('lena.gif')
    img = reduce_rgb(img, 8)
    transformations = compress_rgb(img, 8, 4, 8)
    retrieved_img = decompress_rgb(transformations, 8, 4, 8)
    plt.figure()
    plt.subplot(121)
    plt.imshow(np.array(img).astype(np.uint8), interpolation='none')
    plt.subplot(122)
    plt.imshow(retrieved_img.astype(np.uint8), interpolation='none')
    plt.show()
