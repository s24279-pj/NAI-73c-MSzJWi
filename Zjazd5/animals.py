import tensorflow as tf
import numpy as np


def confusion_matrix(y_true, y_pred, num_classes):
    """
    Tworzy macierz konfuzji dla danych rzeczywistych i przewidywanych.

    Zwraca:
    - Matrycę konfuzji (num_classes x num_classes)
    """
    # Tworzymy pustą macierz konfuzji wypełnioną zerami
    cm = np.zeros((num_classes, num_classes), dtype=int)

    # Iterujemy przez rzeczywiste etykiety i przewidywania
    for true_label, pred_label in zip(y_true, y_pred):
        cm[true_label, pred_label] += 1

    return cm

def filter_animals(X, y):
    """
    Filtruje dane CIFAR-10, pozostawiając tylko klasy zwierząt.
    Zwraca przefiltrowane dane i etykiety.
    """
    # Klasy reprezentujące zwierzęta w CIFAR-10
    animal_classes = [2, 3, 4, 5, 6, 7]  # Odpowiednie etykiety dla zwierząt
    mask = np.isin(y, animal_classes)  # Maska wybierająca tylko zwierzęta
    return X[mask.flatten()], y[mask.flatten()]

def main():
    # Wczytanie danych CIFAR-10
    (X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar10.load_data()

    # Filtrowanie zwierząt
    X_train, y_train = filter_animals(X_train, y_train)
    X_test, y_test = filter_animals(X_test, y_test)

    # Mapowanie etykiet na indeksy 0-5 (dla uproszczenia treningu)
    animal_classes = [2, 3, 4, 5, 6, 7]
    class_mapping = {cls: idx for idx, cls in enumerate(animal_classes)}
    y_train = np.array([class_mapping[label[0]] for label in y_train])
    y_test = np.array([class_mapping[label[0]] for label in y_test])

    # Zmniejszenie rozmiaru obrazów na 28x28
    X_train = tf.image.resize(X_train, (28, 28))
    X_test = tf.image.resize(X_test, (28, 28))

    print("Rozmiar danych treningowych (zwierzęta):", X_train.shape)
    print("Rozmiar danych testowych (zwierzęta):", X_test.shape)

    # Tworzenie modelu
    model = tf.keras.models.Sequential([
        tf.keras.layers.Rescaling(1. / 255),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(6, activation='softmax')  # 6 klas zwierząt
    ])

    optimizer1 = tf.keras.optimizers.Adam(learning_rate=0.0001)

    # Kompilacja modelu
    model.compile(optimizer=optimizer1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    # Trening modelu
    model.fit(X_train, y_train, epochs=20, batch_size=32,
              validation_data=(X_test, y_test))

    # Ocena modelu
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Loss: {loss}, Accuracy: {accuracy}")

    # Wyświetlenie macierzy konfuzji
    cm = confusion_matrix(y_test, y_pred, num_classes=6)
    print("Confusion Matrix:")
    print(cm)

if __name__ == "__main__":
    main()