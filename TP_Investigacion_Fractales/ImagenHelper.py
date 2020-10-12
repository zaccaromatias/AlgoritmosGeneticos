from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import math

# PARAMETROS

directions = [1, -1]
angles = [0, 90, 180, 270]
candidates = [[direction, angle] for direction in directions for angle in angles]


# ----------------------------------------------------------------------------------------------------------------------
#                                                   TRANSFORMACIONES
# ----------------------------------------------------------------------------------------------------------------------


def reduce(img, factor):
    """Reduce el tamaño de la imagen aproximando bloques lindantes"""
    result = np.zeros((img.shape[0] // factor, img.shape[1] // factor))
    for i in range(result.shape[0]):
        for j in range(result.shape[1]):
            result[i, j] = np.mean(img[i * factor:(i + 1) * factor, j * factor:(j + 1) * factor])
    return result


def apply_transformation(img, direction, angle, contrast=1.0, brightness=0.0):
    """Genera las contracciones Rt a partir de los bloques Dj invocando a los métodos rotate(angle) y flip(direction)"""
    return contrast * rotate(flip(img, direction), angle) + brightness


def rotate(img, angle):
    """Rota la imagen según el ángulo dado (sentido antihorario)"""
    return ndimage.rotate(img, angle, reshape=False)


def flip(img, direction):
    """Invierte la imagen si el parámetro es -1"""
    return img[::direction, :]


# ----------------------------------------------------------------------------------------------------------------------
#                                               CONTRASTE Y BRILLO
# ----------------------------------------------------------------------------------------------------------------------


def find_contrast_and_brightness(D, S):
    """Calcula el brillo cuando el contraste es constante"""
    contrast = 0.75
    brightness = (np.sum(D - contrast * S)) / D.size
    return contrast, brightness


def find_contrast_and_brightness2(D, S):
    """Calcula ambos parámetros mediante la técnica de mínimos cuadrados"""
    A = np.concatenate((np.ones((S.size, 1)), np.reshape(S, (S.size, 1))), axis=1)
    b = np.reshape(D, (D.size,))
    x, _, _, _ = np.linalg.lstsq(A, b)
    # x = optimize.lsq_linear(A, b, [(-np.inf, -2.0), (np.inf, 2.0)]).x
    return x[1], x[0]


def generate_all_transformed_blocks(img, source_size, destination_size, step):
    """Genera los bloques Dj y los transforma a bloques Rt. Retorna la lista de bloques Rt"""
    factor = source_size // destination_size
    transformed_blocks = []
    for k in range((img.shape[0] - source_size) // step + 1):
        for l in range((img.shape[1] - source_size) // step + 1):
            # Extract the source block and reduce it to the shape of a destination block
            S = reduce(img[k * step:k * step + source_size, l * step:l * step + source_size], factor)
            # Generate all possible transformed blocks
            for direction, angle in candidates:
                transformed_blocks.append((k, l, direction, angle, apply_transformation(S, direction, angle)))
    return transformed_blocks


def get_transformed(img, k, l, direction, angle, step, source_size, factor):
    S = reduce(img[k * step:k * step + source_size, l * step:l * step + source_size], factor)
    return (k, l, direction, angle, apply_transformation(S, direction, angle))


def get_greyscale_image(img):
    return np.mean(img[:, :, :2], 2)


def plot_iterations(iterations, target=None):
    """Configuración de los plots."""
    plt.figure()
    nb_row = math.ceil(np.sqrt(len(iterations)))
    nb_cols = nb_row
    # Plot
    for i, img in enumerate(iterations):
        plt.subplot(nb_row, nb_cols, i + 1)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255, interpolation='none')
        if target is None:
            plt.title(str(i))
        else:
            # Display the RMSE
            plt.title(str(i))
        frame = plt.gca()
        frame.axes.get_xaxis().set_visible(False)
        frame.axes.get_yaxis().set_visible(False)
    plt.tight_layout()


def IsometricTransform(dirang, img):
    """Genera las contracciones Rt a partir de los bloques Dj."""
    # Rota la imagen según el ángulo dado (sentido antihorario).
    # Invierte la imagen si dirección es -1.
    return ndimage.rotate(img[::dirang[0], :], dirang[1], reshape=False)
