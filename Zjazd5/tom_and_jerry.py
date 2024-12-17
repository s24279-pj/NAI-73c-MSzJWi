import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from tensorflow.keras.utils import to_categorical

def main():
    # Ścieżka do katalogu z obrazami
    data_dir = "tom_and_jerry"  # Główna ścieżka katalogu
    image_size = (32, 32)

    # Wczytanie danych z folderu bez walidacji, tylko trening i test
    dataset = tf.keras.preprocessing.image_dataset_from_directory(
        data_dir,
        image_size=image_size,
        batch_size=32,
        label_mode='int',  # Etykiety są w postaci liczb całkowitych
        shuffle=True,  # Dodajemy tasowanie danych
    )

    # Podział na dane treningowe i testowe (80% treningowe, 20% testowe)
    train_size = int(0.8 * len(dataset.file_paths))
    test_size = len(dataset.file_paths) - train_size

    train_dataset = dataset.take(train_size)
    test_dataset = dataset.skip(train_size)

    # Budowa modelu
    model = tf.keras.models.Sequential([
        tf.keras.layers.Rescaling(1./255),
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(32, 32, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(4, activation='softmax')  # 4 klasy: Tom, Jerry, Both, None
    ])

    # Kompilacja modelu
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])

    # Trenowanie modelu
    model.fit(train_dataset, epochs=50)

    # Ocena modelu na zbiorze testowym
    loss, accuracy = model.evaluate(test_dataset)
    print(f"Test Loss: {loss}, Test Accuracy: {accuracy}")


if __name__ == '__main__':
    main()
