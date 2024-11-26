import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.datasets import fetch_openml

# Pobieramy zbiór danych Abalone z OpenML
abalone = fetch_openml(name='abalone', version=1, as_frame=True)

# Wybieramy dwie cechy: długość (Length) i średnicę (Diameter) muszli
X = abalone.data[['Length', 'Diameter']].values

# Celem jest przewidywanie liczby pierścieni ('Rings') w muszli
y = abalone.target.astype(int)

# Funkcja do klasyfikacji wieku na podstawie liczby pierścieni
# Liczba pierścieni + 1.5 daje wiek muszli
def classify_age(rings):
    """
    Funkcja klasyfikuje muszle na trzy grupy wiekowe:
    0 - Młody (wiek <= 10)
    1 - Średni wiek (10 < wiek <= 15)
    2 - Stary (wiek > 15)

    :param rings: liczba pierścieni w muszli
    :return: numer klasy wiekowej (0, 1, lub 2)
    """
    if rings + 1.5 <= 10:
        return 0  # Młody
    elif rings + 1.5 <= 15:
        return 1  # Średni wiek
    else:
        return 2  # Stary


# Stosujemy funkcję do podziału na klasy wiekowe
y_classified = np.array([classify_age(r) for r in y])

# Tworzymy model SVM z jądrem RBF (radial basis function)
svc = svm.SVC(kernel='rbf', C=1, gamma=100).fit(X, y_classified)

# Zakres danych: rozszerzamy go o 0.3 jednostki, aby uzyskać przestrzeń dla granic decyzyjnych
x_min, x_max = X[:, 0].min() - 0.3, X[:, 0].max() + 0.3
y_min, y_max = X[:, 1].min() - 0.3, X[:, 1].max() + 0.3
h = (x_max - x_min) / 100  # Rozdzielczość wykresu
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# Predykcja na siatce punktów
plt.subplot(1, 1, 1)
Z = svc.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Rysowanie granic decyzyjnych z 3 klasami
plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)

# Rysowanie punktów danych z przypisanymi kolorami dla trzech klas
scatter = plt.scatter(X[:, 0], X[:, 1], c=y_classified, cmap=plt.cm.Paired)

# Etykiety osi i tytuł wykresu
plt.xlabel('Abalone Length')
plt.ylabel('Abalone Diameter')
plt.xlim(xx.min(), xx.max())  # Dostosowanie granic osi x
plt.title('SVC with RBF kernel (Age Classification)')

# Dodanie legendy, która opisuje klasy wiekowe
handles, labels = scatter.legend_elements()
plt.legend(handles, ['Young', 'Middle Age', 'Old'])

# Wyświetlanie wykresu
plt.show()
