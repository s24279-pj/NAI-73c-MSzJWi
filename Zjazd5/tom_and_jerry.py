import tensorflow as tf


def main():

    data_dir = "tom_and_jerry"
    image_size = (32, 32)

    """
    Załadowanie danych treningowych z katalogu 'tom_and_jerry'.
    Dane są przeskalowane do rozmiaru 32x32 piksele, podzielone na partie o wielkości 32 (batch_size),
    z 20% danych przeznaczonych na walidację.
    """
    train_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,  # Katalog z danymi
        image_size=image_size,  # Rozmiar obrazów
        batch_size=32,  # Wielkość partii danych
        label_mode='int',  # Typ etykiet (liczby całkowite)
        shuffle=True,  # Losowe mieszanie danych
        validation_split=0.2,  # Podział danych na zbiór treningowy i walidacyjny (80% - 20%)
        subset="training",  # Ustal zbiór na treningowy
        seed=1337  # Ustal ziarno dla powtarzalności
    )

    """
    Załadowanie danych walidacyjnych z katalogu 'tom_and_jerry'.
    Dane są przeskalowane do rozmiaru 32x32 piksele, z takim samym podziałem jak w przypadku zbioru treningowego.
    """
    test_dataset = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,  # Katalog z danymi
        image_size=image_size,  # Rozmiar obrazów
        batch_size=32,  # Wielkość partii danych
        label_mode='int',  # Typ etykiet (liczby całkowite)
        shuffle=True,  # Losowe mieszanie danych
        validation_split=0.2,  # Podział danych na zbiór treningowy i walidacyjny (80% - 20%)
        subset="validation",  # Ustal zbiór na walidacyjny
        seed=1337  # Ustal ziarno dla powtarzalności
    )

    print(f"Rozmiar zbioru treningowego: {len(train_dataset)}")
    print(f"Rozmiar zbioru walidacyjnego: {len(test_dataset)}")

    """
    Budowa modelu sieci neuronowej typu CNN.
    Model składa się z dwóch warstw konwolucyjnych z aktywacją ReLU, warstw MaxPooling,
    warstwy Flatten, pełnej warstwy Dense z 128 neuronami oraz warstwy Dropout dla zapobiegania przeuczeniu.
    Warstwa wyjściowa ma 4 neurony z funkcją aktywacji softmax dla klasyfikacji wieloklasowej.
    """
    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(shape=(32, 32, 3)),  # Definicja wejścia modelu (obrazy 32x32x3)
        tf.keras.layers.Rescaling(1. / 255),  # Normalizacja pikseli obrazu do zakresu [0, 1]
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),  # Pierwsza warstwa konwolucyjna
        tf.keras.layers.MaxPooling2D((2, 2)),  # Warstwa MaxPooling zmniejszająca rozmiar obrazu
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu'),  # Druga warstwa konwolucyjna
        tf.keras.layers.MaxPooling2D((2, 2)),  # Druga warstwa MaxPooling
        tf.keras.layers.Flatten(),  # Spłaszczenie danych do wektora
        tf.keras.layers.Dense(128, activation='relu'),  # Pełna warstwa Dense z 128 neuronami
        tf.keras.layers.Dropout(0.2),  # Warstwa Dropout dla zapobiegania przeuczeniu
        tf.keras.layers.Dense(4, activation='softmax')  # Warstwa wyjściowa z 4 klasami
    ])

    """
    Kompilacja modelu.
    """
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    """
    Trenowanie modelu na danych treningowych przez 20 epok.
    Zbiór walidacyjny jest używany do oceny modelu w trakcie treningu.
    """
    model.fit(train_dataset, epochs=20, batch_size=32, validation_data=test_dataset)

    """
    Ocena modelu na zbiorze walidacyjnym. Wyświetlenie wartości straty i dokładności.
    """
    loss, accuracy = model.evaluate(test_dataset)
    print(f"Strata testowa: {loss}, Dokładność testowa: {accuracy}")


if __name__ == '__main__':
    main()
