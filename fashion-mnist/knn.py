import numpy as np

NUMBER_OF_CLASSES = 10


def distance_function(x, x_train):
    return np.array([[np.linalg.norm(test_o - train_o) for train_o in x_train] for test_o in x])


def sort_train_labels_knn(distance, labels):
    return labels[np.argsort(distance)]


def p_y_x_knn(y, k):
    return np.array([np.bincount(row[:k], minlength=NUMBER_OF_CLASSES) for row in y]) / k


def classification_error(p_y_x, y_true):
    y_pred = [np.argmax(row) for row in p_y_x]
    return sum(y_pred[i] != y_true[i] for i in range(y_true.shape[0])) / len(y_true)


def knn_model_selection(x_val, x_train, y_val, y_train, k_values):
    labels = sort_train_labels_knn(distance_function(x_val, x_train), y_train)
    prediction = [p_y_x_knn(labels, k) for k in k_values]
    errors = [classification_error(pred, y_val) for pred in prediction]
    min_error_index = np.argmin(errors)
    return dict(zip(k_values, errors)), k_values[min_error_index]


def knn_test(x_train, x_test, y_train, y_test, k):
    labels = sort_train_labels_knn(distance_function(x_test, x_train), y_train)
    return classification_error(p_y_x_knn(labels, k), y_test)


def run_training(train_images, train_labels, test_images, test_labels):

    train_images = train_images / 255.0
    test_images = test_images / 255.0

    train_set = train_images[:10000, :]
    train_set_labels = train_labels[:10000]
    val_set = train_images[10000:12000, :]
    val_set_labels = train_labels[10000:12000]

    test_set_half = test_images[:5000, :]
    test_set_half_labels = test_labels[:5000]
    train_set_half = train_images[:30000, :]
    train_set_half_labels = train_labels[:30000]

    # models, best_k = knn_model_selection(val_set, train_set, val_set_labels, train_set_labels, [1, 5, 9])
    # print(models)

    # full test:
    print(knn_test(train_set_half, test_set_half, train_set_half_labels, test_set_half_labels, 5))
