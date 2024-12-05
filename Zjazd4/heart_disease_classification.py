import numpy as np
import matplotlib.pyplot as plt
from sklearn import svm
from sklearn.metrics import confusion_matrix, accuracy_score
import pandas as pd
from utilities_hd import visualize_classifier


# Wczytanie i przygotowanie danych
data = pd.read_csv("heart.csv", header=0)
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

# Wybór cech wejściowych i zmiennej docelowej
X = data[['age', 'chol']].values
y = data[['output']].values.ravel()

# Tworzymy model SVM z jądrem RBF (radial basis function)
svc = svm.SVC(kernel='rbf', C=1, gamma=50).fit(X, y)

# Wizualizacja wyników klasyfikacji
visualize_classifier(svc, X, y, 'SVC with RBF kernel (HeartDisease)')

# Przykładowe dane wejściowe
sample_data = np.array([[60, 282]])

# Przewidywanie klasy dla przykładowych danych
predicted_class = svc.predict(sample_data)

# Etykiety klas
health_labels = ['Healthy', 'Diseased']

# Wyświetlanie wyniku klasyfikacji dla przykładowych danych
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
