import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.datasets import fetch_openml

from utilities import visualize_classifier

# Pobieramy zbiór danych Abalone z OpenML
abalone = fetch_openml(name='abalone', version=1, as_frame=True)

# Wybieramy dwie cechy: długość (Length) i średnicę (Diameter) muszli
# Wybieramy dwie cechy, aby łatwiej przedstawić dane na dwuwymiarowym wykresie
X = abalone.data[['Length', 'Diameter']].values

# Celem jest przewidywanie liczby pierścieni ('Rings') w muszli
y = abalone.target.astype(int)

def classify_age(rings):
    """
    Funkcja klasyfikuje muszle na trzy grupy wiekowe:
    0 - Młody (wiek <= 8)
    1 - Średni wiek (8 < wiek <= 12)
    2 - Stary (wiek > 12)

    :param rings: liczba pierścieni w muszli
    :return: numer klasy wiekowej (0, 1, lub 2)
    """
    if rings + 1.5 <= 8:
        return 0  # Młody 's'
    elif rings + 1.5 <= 12:
        return 1  # Średni wiek 'x'
    else:
        return 2  # Stary 'o'


# Stosujemy funkcję do podziału na klasy wiekowe
y_classified = np.array([classify_age(r) for r in y])


# Podział danych według klas wiekowych
class_0 = np.array(X[y_classified==0])
class_1 = np.array(X[y_classified==1])
class_2 = np.array(X[y_classified==2])

# Wizualizacja danych wejściowych
plt.figure()
plt.scatter(class_0[:, 0], class_0[:, 1], s=75, facecolors='white', edgecolors='black',
            linewidth=1, marker='s', label='Young')
plt.scatter(class_1[:, 0], class_1[:, 1], s=75, facecolors='black',
            linewidth=1, marker='x', label='Middle Age')
plt.scatter(class_2[:, 0], class_2[:, 1], s=75, facecolors='white', edgecolors='black', linewidth=1, marker='o', label='Old')
plt.title('Input data')
plt.xlabel('Length')
plt.ylabel('Diameter')
plt.legend()

# Podział bazy danych na zbiór testowy i treningowy
X_train, X_test, y_train, y_test = train_test_split(
        X, y_classified, test_size=0.25, random_state=42)

# Konfiguracja i trening klasyfikatora drzewa decyzyjnego
params = {'random_state': 42, 'max_depth': 16}
classifier = DecisionTreeClassifier(**params)

# Wizualizacja klasyfikacji na zbiorze treningowym
classifier.fit(X_train, y_train)
visualize_classifier(classifier, X_train, y_train, 'Training dataset')

# Predykcja i wizualizacja na zbiorze testowym
y_test_pred = classifier.predict(X_test)
visualize_classifier(classifier, X_test, y_test, 'Test dataset')

# Wyświetlenie raportu z wynikami klasyfikacji
class_names = ['Young', 'Middle Age', 'Old']
print("\n" + "#"*40)
print("\nClassifier performance on training dataset\n")
print(classification_report(y_train, classifier.predict(X_train), target_names=class_names))
print("#"*40 + "\n")

print("#"*40)
print("\nClassifier performance on test dataset\n")
print(classification_report(y_test, y_test_pred, target_names=class_names))
print("#"*40 + "\n")

plt.show()