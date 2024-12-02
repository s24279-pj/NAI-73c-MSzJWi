import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from utilities_hd import visualize_classifier

data = pd.read_csv("heart.csv", header=0)
data = data.sample(frac=1, random_state=42).reset_index(drop=True)

X = data[['age', 'chol']].values
y = data[['output']].values.ravel()

healthy = X[y==0]
diseased = X[y==1]

plt.figure()
plt.scatter(healthy[:,0],healthy[:,1], s=75, edgecolors='black',facecolor = 'white', linewidths=1,
            marker='o', label='Healthy')
plt.scatter(diseased[:,0],diseased[:,1], s=75,facecolor = 'red', linewidths=1,
            marker='x', label='Diseased')
plt.title('Input data')
plt.xlabel('Age')
plt.ylabel('Cholesterol')
plt.legend()
plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

params = {'random_state': 42,'max_depth': 5}
classifier = DecisionTreeClassifier(**params)
classifier.fit(X_train, y_train)
visualize_classifier(classifier, X_train, y_train, 'Training dataset')

y_pred = classifier.predict(X_test)
visualize_classifier(classifier, X_test, y_test, 'Test dataset')

class_names = ['Healthy', 'Diseased']
print("\n" + "#"*40)
print("\nClassifier performance on training dataset\n")
print(classification_report(y_train, classifier.predict(X_train), target_names=class_names))
print("#"*40 + "\n")

print("#"*40)
print("\nClassifier performance on test dataset\n")
print(classification_report(y_test, y_pred, target_names=class_names))
print("#"*40 + "\n")

plt.show()