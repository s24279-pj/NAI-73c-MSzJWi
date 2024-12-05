import numpy as np
import matplotlib.pyplot as plt

def visualize_classifier(classifier, X, y, title=''):

    # Definiowanie minimalnych i maksymalnych wartości dla X i Y do siatki
    min_x, max_x = X[:, 0].min() - 0.2, X[:, 0].max() + 0.2
    min_y, max_y = X[:, 1].min() - 0.2, X[:, 1].max() + 0.2

    # Definiowanie kroku siatki
    mesh_step_size = 0.01

    # Tworzenie siatki punktów
    x_vals, y_vals = np.meshgrid(np.arange(min_x, max_x, mesh_step_size), np.arange(min_y, max_y, mesh_step_size))

    # Klasyfikacja punktów siatki
    output = classifier.predict(np.c_[x_vals.ravel(), y_vals.ravel()])

    # Dopasowanie wymiarów wyników do siatki
    output = output.reshape(x_vals.shape)

    # Tworzenie wykresu
    plt.figure()

    # Nadanie tytułu
    plt.title(title)

    # Wizualizacja granic decyzyjnych z kolorami dla różnych klas
    plt.pcolormesh(x_vals, y_vals, output, cmap=plt.cm.Paired)

    # Nałożenie punktów danych treningowych na wykres
    scatter = plt.scatter(X[:, 0], X[:, 1], c=y, s=75, edgecolors='black', linewidth=1, cmap=plt.cm.Paired)

    # Dodanie etykiet osi
    plt.xlabel('Abalone Length')
    plt.ylabel('Abalone Diameter')

    # Dodanie legendy, która opisuje klasy wiekowe
    handles, labels = scatter.legend_elements()
    plt.legend(handles, ['Young', 'Middle Age', 'Old'])

    # Określenie granic osi
    plt.xlim(x_vals.min(), x_vals.max())
    plt.ylim(y_vals.min(), y_vals.max())

    # Dodanie oznaczeń osi
    plt.xticks((np.arange(int(X[:, 0].min() - 0.2), int(X[:, 0].max() + 1), 0.2)))
    plt.yticks((np.arange(int(X[:, 1].min() - 0.2), int(X[:, 1].max() + 1), 0.2)))

    # Dodanie oznaczeń osi
    plt.show()
