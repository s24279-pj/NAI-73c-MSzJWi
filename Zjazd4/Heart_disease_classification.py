import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.metrics import confusion_matrix, accuracy_score
import pandas as pd


data = pd.read_csv("heart.csv", header=0)
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

X = data[['age', 'chol']].values

y = data[['output']].values.ravel()

svc = svm.SVC(kernel='rbf', C=1, gamma=50).fit(X, y)

# Tworzymy model SVM z jądrem RBF (radial basis function)
svc = svm.SVC(kernel='rbf', C=1, gamma=50).fit(X, y)

# Zakres danych: rozszerzamy go o odpowiednie jednostki, aby uzyskać przestrzeń dla granic decyzyjnych
x_min, x_max = X[:, 0].min() - 5, X[:, 0].max() + 5
y_min, y_max = X[:, 1].min() - 20, X[:, 1].max() + 20
h = (x_max - x_min) / 100  # Rozdzielczość wykresu
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))

# Predykcja na siatce punktów
plt.subplot(1, 1, 1)
#Przewidywanie klas na siatce punktów w celu wizualizacji granic decyzyjnych.
#ravel() spłaszcza siatkę (macierz) do wektora.
Z = svc.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

# Rysowanie granic decyzyjnych
plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)

# Rysowanie punktów danych z kolorami zgodnymi z wartościami y
scatter = plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Paired, edgecolors='k')

# Etykiety osi i tytuł wykresu
plt.xlabel('Age')
plt.ylabel('Cholesterol')
plt.xlim(xx.min(), xx.max())  # Dostosowanie granic osi x
plt.title('SVC with RBF kernel (HeartDisease)')

# Dodanie legendy
legend_labels = ['Healthy', 'Diseased']  # Odpowiednie etykiety dla wartości 0 i 1
handles, labels = scatter.legend_elements()
plt.legend(handles, legend_labels, title="Condition")

# Wyświetlanie wykresu
plt.show()

# Przykładowe dane wejściowe
sample_data = np.array([[60, 282]])

# Wywołanie klasyfikatora
predicted_class = svc.predict(sample_data)

# Etykiety klas
health_labels = ['Healthy', 'Diseased']

# Wyświetlanie wyniku
print(f"Predicted class for sample data {sample_data[0]}: {health_labels[predicted_class[0]]}")

# Przewidywanie klas dla całego zbioru danych
y_pred = svc.predict(X)

# Wyświetlenie macierzy konfuzji
conf_matrix = confusion_matrix(y, y_pred)
print("Confusion Matrix:")
print(conf_matrix)

# Obliczenie dokładności klasyfikacji
accuracy = accuracy_score(y, y_pred)
print(f"Accuracy: {accuracy:.2f}")
