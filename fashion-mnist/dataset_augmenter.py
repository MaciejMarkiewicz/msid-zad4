import numpy as np
from scipy.ndimage.filters import gaussian_filter
from scipy.ndimage.interpolation import map_coordinates
from tensorflow import keras


def elastic_transform(image, alpha_range, sigma, random_state=None):
    if random_state is None:
        random_state = np.random.RandomState(None)

    if np.isscalar(alpha_range):
        alpha = alpha_range
    else:
        alpha = np.random.uniform(low=alpha_range[0], high=alpha_range[1])

    shape = image.shape
    dx = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha
    dy = gaussian_filter((random_state.rand(*shape) * 2 - 1), sigma) * alpha

    x, y, z = np.meshgrid(np.arange(shape[0]), np.arange(shape[1]), np.arange(shape[2]), indexing='ij')
    indices = np.reshape(x + dx, (-1, 1)), np.reshape(y + dy, (-1, 1)), np.reshape(z, (-1, 1))

    return map_coordinates(image, indices, order=1, mode='reflect').reshape(shape)


def data_generator():
    return keras.preprocessing.image.ImageDataGenerator(
        width_shift_range=0,
        height_shift_range=0,
        zoom_range=0.0,
        preprocessing_function=lambda image: elastic_transform(image, alpha_range=8, sigma=3)
    )


def image_augmentation(image, datagen, number_of_augmentations):
    images = []
    image = image.reshape(1, 28, 28, 1)
    i = 0

    for x_batch in datagen.flow(image, batch_size=1):
        images.append(x_batch)
        i += 1
        if i >= number_of_augmentations:
            return images


def preprocess_data(train_images, train_labels, test_images, test_labels):
    datagen = data_generator()

    preprocessed_x = []
    preprocessed_y = []

    for image, label in zip(train_images, train_labels):
        augmented_images = image_augmentation(image, datagen, 2)

        for aug_image in augmented_images:
            preprocessed_x.append(aug_image.reshape(28, 28, 1))
            preprocessed_y.append(label)

        preprocessed_x.append(image.reshape(28, 28, 1))
        preprocessed_y.append(label)

    preprocessed_x = np.array(preprocessed_x) / 255
    test_images = (test_images / 255).reshape(len(test_images), 28, 28, 1)

    return preprocessed_x, keras.utils.to_categorical(preprocessed_y), test_images, \
           keras.utils.to_categorical(test_labels)
