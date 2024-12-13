import pandas as pd
import tensorflow as tf

def main():
    """
       Wczytuje dane z pliku CSV, ustawia odpowiednie nagłówki dla kolumn.
    """
    data = pd.read_csv("heart.csv", header=0)
    data.columns = ['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBloodSugar', 'RestingECG',
                    'MaxHeartRateAchieved', 'ExerciseInducedAngina', 'Oldpeak', 'Slope', 'NumberOfMajorVessels',
                    'Thalassemia', 'HeartDisease']

    """
       Przetasowuje dane, aby zapewnić losowy rozkład przypadków w zbiorze.
    """
    data = data.sample(frac=1, random_state=42).reset_index(drop=True)

    """
    Oddzielenie cech od etykiety:
       Usuwamy kolumnę 'HeartDisease' z danych, reszta to nasze cechy (X), 
       a etykieta (y) to wartości z kolumny 'HeartDisease'.
    """
    X = data.drop('HeartDisease', axis=1)
    y = data[['HeartDisease']].values.ravel()

    """
        Podział danych na zbiory treningowy i testowy:
       Ustal proporcję podziału danych, np. 80% dla treningu, 20% dla testu.
    """
    train_size = int(0.8 * len(X))  # 80% dla treningu
    test_size = len(X) - train_size  # 20% dla testu

    X_train, y_train = X.iloc[:train_size], y[:train_size]
    X_test, y_test = X.iloc[train_size:], y[train_size:]

    """
       Tworzy model sieci neuronowej z dwoma warstwami Dense, Dropout dla regularizacji
       oraz warstwą wyjściową z funkcją aktywacji 'sigmoid' dla klasyfikacji binarnej.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.1),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    """
       Tworzy optymalizator Adam z określoną stopą uczenia.
    """
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)

    """
       Kompiluje model z funkcją straty 'binary_crossentropy' oraz metryką 'accuracy'.
    """
    model.compile(optimizer=optimizer, loss='binary_crossentropy', metrics=['accuracy'])

    """
       Trenuje model na danych treningowych przez 50 epok z wykorzystaniem
       zbioru testowego do walidacji.
    """
    model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

    """
        Ocena modelu na danych testowych. Zwracana jest strata oraz dokładność.
    """
    loss, accuracy = model.evaluate(X_test, y_test)
    print(f"Model 1 - Loss: {loss}, Accuracy: {accuracy}")

if __name__ == "__main__":
    main()
