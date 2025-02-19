import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt


def confusion_matrix(y_true, y_pred, num_classes):
    """
    Tworzy macierz konfuzji, porównując prawdziwe etykiety z przewidywanymi.

    Argumenty:
        y_true (array-like): Tablica prawdziwych etykiet klas.
        y_pred (array-like): Tablica przewidywanych etykiet klas.
        num_classes (int): Liczba klas w zadaniu klasyfikacyjnym.

    Zwraca:
        np.ndarray: Macierz konfuzji jako dwuwymiarowa tablica, gdzie każdy element [i, j] 
                    reprezentuje liczbę przypadków, w których klasa i została przewidziana 
                    jako klasa j.
    """
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for true_label, pred_label in zip(y_true, y_pred):
        cm[true_label, pred_label] += 1
    return cm

def main():
    """
    Główna funkcja, która ładuje zbiór danych Fashion MNIST, przetwarza go,
    trenuje dwa różne modele (mniejszy i większy), ocenia je,
    a następnie wypisuje macierze konfuzji.
    """

    """
    Ładowanie zbioru danych Fashion MNIST.
    """
    (X_train, y_train), (X_test, y_test) = tf.keras.datasets.fashion_mnist.load_data()

    """
    Normalizacja danych wejściowych (0-1)
    """
    X_train = X_train / 255.0
    X_test = X_test / 255.0

    """
    # Zmiana kształtu danych (dodanie wymiaru kanałów)
    """
    X_train = X_train[..., np.newaxis]
    X_test = X_test[..., np.newaxis]

    """
    # Wydrukowanie kształtów danych
    """
    print("Rozmiar danych treningowych:", X_train.shape)
    print("Rozmiar danych testowych:", X_test.shape)

    """
    # Modele o różnych rozmiarach
    """

    model_1 = build_model_small()  # Mniejszy model
    model_2 = build_model_large()  # Większy model

    """
    # Kompilacja modeli
    """
    optimizer1 = tf.keras.optimizers.Adam(learning_rate=0.0001)
    optimizer2 = tf.keras.optimizers.Adam(learning_rate=0.0001)
    model_1.compile(optimizer=optimizer1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model_2.compile(optimizer=optimizer2, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    """
    # Trening obu modeli
    """
    print("Trening modelu 1...")
    model_1.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

    print("Trening modelu 2...")
    model_2.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test))

    """
    # Ocena obu modeli
    """
    loss_1, acc_1 = model_1.evaluate(X_test, y_test)
    loss_2, acc_2 = model_2.evaluate(X_test, y_test)

    print(f"Model 1 - Loss: {loss_1}, Accuracy: {acc_1}")
    print(f"Model 2 - Loss: {loss_2}, Accuracy: {acc_2}")

    """
    # Przewidywania
    """
    y_pred_1 = np.argmax(model_1.predict(X_test), axis=1)
    y_pred_2 = np.argmax(model_2.predict(X_test), axis=1)

    """
    # Wyświetlenie macierzy konfuzji
    """
    cm_1 = confusion_matrix(y_test, y_pred_1, num_classes=10)
    cm_2 = confusion_matrix(y_test, y_pred_2, num_classes=10)

    print("Macierz konfuzji dla modelu 1:")
    print(cm_1)

    print("Macierz konfuzji dla modelu 2:")
    print(cm_2)


def build_model_small():
    """
    Buduje mniejszy model sieci neuronowej splotowej do klasyfikacji obrazów.

    Model składa się z:
        - Warstwy konwolucyjnej z 32 filtrami i jądrem 3x3.
        - Warstwy max-pooling z rozmiarem 2x2.
        - Warstwy dropout o współczynniku 0.2, aby zapobiec przeuczeniu.
        - Warstwy gęstej z 64 jednostkami i aktywacją ReLU.
        - Warstwy wyjściowej z 10 jednostkami (po jednej na każdą klasę) i aktywacją softmax.

    Zwraca:
        tf.keras.models.Sequential: Skompilowany mały model gotowy do treningu.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')  # 10 klas ubrań
    ])
    return model

def build_model_large():
    """
    Buduje większy model sieci neuronowej splotowej do klasyfikacji obrazów.

    Model składa się z:
        - Warstwy konwolucyjnej z 64 filtrami i jądrem 3x3.
        - Warstwy max-pooling z rozmiarem 2x2.
        - Drugiej warstwy konwolucyjnej z 128 filtrami i jądrem 3x3.
        - Drugiej warstwy max-pooling z rozmiarem 2x2.
        - Warstwy dropout o współczynniku 0.4, aby zapobiec przeuczeniu.
        - Warstwy gęstej z 256 jednostkami i aktywacją ReLU.
        - Warstwy wyjściowej z 10 jednostkami (po jednej na każdą klasę) i aktywacją softmax.

    Zwraca:
        tf.keras.models.Sequential: Skompilowany większy model gotowy do treningu.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu', input_shape=(28, 28, 1)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Dropout(0.4),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')  # 10 klas ubrań
    ])
    return model

if __name__ == "__main__":
    main()
