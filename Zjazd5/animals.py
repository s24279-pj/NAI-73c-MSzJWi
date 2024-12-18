import tensorflow as tf
import numpy as np


def confusion_matrix(y_true, y_pred, num_classes):
    """
    Tworzy macierz konfuzji dla danych rzeczywistych i przewidywanych.

    Argumenty:
    - y_true: rzeczywiste etykiety (w formie wektora).
    - y_pred: przewidywane etykiety (w formie wektora).
    - num_classes: liczba klas (np. dla klasyfikacji binarnej będzie to 2).

    Zwraca:
    - Macierz konfuzji (num_classes x num_classes), gdzie każda komórka
      zawiera liczbę przypadków danego połączenia rzeczywistej etykiety i
      przewidywanej etykiety.
    """
    cm = np.zeros((num_classes, num_classes), dtype=int)
    for true_label, pred_label in zip(y_true, y_pred):
        cm[true_label, pred_label] += 1
    return cm


def filter_animals(X, y):
    """
    Filtruje dane CIFAR-10, pozostawiając tylko klasy zwierząt.

    Argumenty:
    - X: dane wejściowe (obrazy).
    - y: etykiety klas.

    Zwraca:
    - Przefiltrowane dane X i y, zawierające tylko klasy zwierząt.
    """
    animal_classes = [2, 3, 4, 5, 6, 7]
    mask = np.isin(y, animal_classes)
    return X[mask.flatten()], y[mask.flatten()]


def main():

    """
    Wczytuje dane z zestawu CIFAR-10, który zawiera obrazy 10 różnych klas.
    Zwraca dane treningowe i testowe.
    """
    (X_train, y_train), (X_test, y_test) = tf.keras.datasets.cifar10.load_data()

    """
    Filtruje dane, pozostawiając tylko obrazy przedstawiające zwierzęta (klasy 2-7).
    Zwraca przefiltrowane dane X i y.
    """
    X_train, y_train = filter_animals(X_train, y_train)
    X_test, y_test = filter_animals(X_test, y_test)

    """
    Mapuje oryginalne etykiety klas zwierząt na indeksy 0-5.
    Pozwala to na uproszczenie problemu klasyfikacji do 6 klas.
    """
    animal_classes = [2, 3, 4, 5, 6, 7]
    class_mapping = {cls: idx for idx, cls in enumerate(animal_classes)}
    y_train = np.array([class_mapping[label[0]] for label in y_train])
    y_test = np.array([class_mapping[label[0]] for label in y_test])

    """
    Zmienia rozmiar obrazów z oryginalnego 32x32 na 28x28 w celu przystosowania do modelu.
    """
    X_train = tf.image.resize(X_train, (28, 28))
    X_test = tf.image.resize(X_test, (28, 28))

    print("Rozmiar danych treningowych (zwierzęta):", X_train.shape)
    print("Rozmiar danych testowych (zwierzęta):", X_test.shape)

    """
    Tworzy model sieci neuronowej z warstwami Conv2D, MaxPooling, Flatten, Dense oraz Dropout.
    Model wykorzystuje funkcję aktywacji ReLU w warstwach ukrytych oraz softmax w warstwie wyjściowej.
    """
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

    """
    Tworzy optymalizator Adam z określoną stopą uczenia.
    Adam jest popularnym optymalizatorem w sieciach neuronowych.
    """
    optimizer1 = tf.keras.optimizers.Adam(learning_rate=0.0001)

    """
    Kompiluje model z funkcją straty oraz metryką 'accuracy', która mierzy dokładność klasyfikacji.
    """
    model.compile(optimizer=optimizer1, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    """
    Trenuje model na danych treningowych przez 30 epok, używając danych testowych do walidacji.
    """
    model.fit(X_train, y_train, epochs=30, batch_size=32, validation_data=(X_test, y_test))

    """
    Ocenia model na danych testowych i wyświetla wynik (strata i dokładność).
    """
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Loss: {loss}, Accuracy: {accuracy}")

    """
    Przewiduje wyniki na zbiorze testowym oraz oblicza i wyświetla macierz konfuzji.
    """
    y_pred = model.predict(X_test)
    y_pred = np.argmax(y_pred, axis=1)
    cm = confusion_matrix(y_test, y_pred, num_classes=6)
    print("Confusion Matrix:")
    print(cm)


if __name__ == "__main__":
    main()
