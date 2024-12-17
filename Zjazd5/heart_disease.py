import pandas as pd
import tensorflow as tf
import numpy as np


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
    Wczytuje dane z pliku CSV, ustawia odpowiednie nagłówki dla kolumn.
    Plik CSV zawiera dane dotyczące chorób serca, gdzie każda kolumna odpowiada różnym cechom pacjenta.
    """
    data = pd.read_csv("heart.csv", header=0)
    data.columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBloodSugar', 'RestingECG',
                    'MaxHeartRateAchieved', 'ExerciseInducedAngina', 'Oldpeak', 'Slope', 'NumberOfMajorVessels',
                    'Thalassemia', 'HeartDisease']

    """
    Przetasowuje dane, aby zapewnić losowy rozkład przypadków w zbiorze.
    Funkcja `sample` losowo przetasowuje dane, aby upewnić się, że dane są równomiernie rozłożone w zbiorach treningowym i testowym.
    """
    data = data.sample(frac=1, random_state=42).reset_index(drop=True)

    """
    Oddziela cechy (X) od etykiety (y):
    - Usuwamy kolumnę 'HeartDisease' z danych, traktując ją jako etykietę (y).
    - Pozostałe kolumny traktujemy jako cechy wejściowe (X).
    """
    X = data.drop('HeartDisease', axis=1)
    y = data[['HeartDisease']].values.ravel()

    """
    Podział danych na zbiory treningowy i testowy:
    - Ustalamy proporcję podziału danych, np. 70% danych na zbiór treningowy, 30% na zbiór testowy.
    - `train_size` to liczba próbek w zbiorze treningowym.
    - `test_size` to liczba próbek w zbiorze testowym.
    """
    train_size = int(0.7 * len(X))  # 70% dla treningu
    test_size = len(X) - train_size  # 30% dla testu

    X_train, y_train = X.iloc[:train_size], y[:train_size]
    X_test, y_test = X.iloc[train_size:], y[train_size:]

    """
    Tworzy model sieci neuronowej z dwoma warstwami Dense, Dropout dla regularizacji
    oraz warstwą wyjściową z funkcją aktywacji 'sigmoid' do klasyfikacji binarnej.
    Model ten jest stosunkowo prosty, składający się z dwóch warstw ukrytych.
    Dodano również warstwę BatchNormalization, która normalizuje dane wejściowe do kolejnych warstw,
    aby przyspieszyć proces uczenia oraz zwiększyć stabilność i efektywność modelu.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    """
    Tworzy optymalizator Adam z określoną stopą uczenia dla modelu.
    Optymalizator Adam jest popularnym wyborem dla modeli neuronowych dzięki swojej efektywności.
    """
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.0001)

    """
    Kompiluje model z funkcją straty 'binary_crossentropy' oraz metryką 'accuracy'.
    Funkcja straty 'binary_crossentropy' jest stosowana w klasyfikacji binarnej, a 'accuracy' mierzy dokładność modelu.
    """
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    """
    Trenuje model na danych treningowych przez 50 epok, używając danych testowych do walidacji.
    """
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    """
    Ocena modelu na danych testowych. Zwróci się strata oraz dokładność modelu.
    """
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Model - Loss: {loss}, Accuracy: {accuracy}")

    """
    Przewidywanie wyników dla zbioru testowego na podstawie modelu.
    Wynik jest zaokrąglany do wartości 0 lub 1 (klasyfikacja binarna).
    """
    y_pred = (model.predict(X_test) > 0.5).astype(int).flatten()

    """
    Obliczenie i wyświetlenie macierzy konfuzji
    """
    cm = confusion_matrix(y_test, y_pred, num_classes=2)
    print("Macierz konfuzji:")
    print(cm)


if __name__ == "__main__":
    main()
