# Neural Networks for Image Classification and Heart Disease Prediction

## Project Description

This project demonstrates the use of neural networks for two distinct tasks:

1. **Animal Image Classification**: A convolutional neural network (CNN) is applied to classify images of animals from the CIFAR-10 dataset.
2. **Clothing Image Classification**: A CNN is used for classifying images of clothing from the Fashion MNIST dataset.
3. **Heart Disease Prediction**: A feedforward neural network (FNN) is used to predict the presence of heart disease based on patient data.

Each model is evaluated using various performance metrics such as accuracy, loss, confusion matrix, and classification reports.

## Project Structure

### Files and Scripts

- `animals.py`: Classifies images of animals from the CIFAR-10 dataset. It filters the dataset to include only animal classes and trains a CNN model.
- `clothes.py`: Classifies images from the Fashion MNIST dataset using two different CNN architectures (small and large).
- `heart_disease.py`: Predicts heart disease presence using a feedforward neural network. The dataset used contains various medical attributes like age, cholesterol level, and more.
- `heart.csv`: CSV file containing patient data for the heart disease classification task.
- README.md: Documentation for the project (this file).

### Datasets

1. **CIFAR-10 Dataset**: A dataset containing 60,000 32x32 color images in 10 classes, with a focus on animal-related classes.
   - Animal classes: bird, cat, deer, dog, frog, and horse.
2. **Fashion MNIST Dataset**: A dataset of 60,000 28x28 grayscale images of 10 clothing items.
3. **Heart Disease Dataset**: A dataset of 303 records with 14 features used to predict the presence or absence of heart disease.

## Usage

### Requirements

To run the scripts, make sure you have the following Python packages installed:

- `numpy`
- `tensorflow`
- `matplotlib`
- `pandas`

You can install them using `pip`:

```bash
pip install numpy tensorflow matplotlib pandas
```

### Evaluation Metrics

For each model, the following evaluation metrics are computed:

- **Confusion Matrix**: A matrix showing the counts of true positive, false positive, true negative, and false negative classifications.
- **Accuracy**: The ratio of correct predictions to total predictions.

## Running the Scripts

### Animal Image Classification (CIFAR-10)

Run the script `animals.py` to classify animal images from the CIFAR-10 dataset.

Command:
```bash
python animals.py
```

#### Output
The script will display:
- The model's accuracy and loss on the test dataset.
- The confusion matrix for the predictions.

### Clothing Image Classification (Fashion MNIST)

Run the script `clothes.py` to classify images of clothing from the Fashion MNIST dataset. This script uses two models with different architectures (small and large) for classification.

#### Command to run the small model:
```bash
python clothes.py
```

#### Output
- Displays accuracy and loss for both models.
- Prints confusion matrices for both models.

### Heart Disease Prediction

Run the script `heart_disease.py` to predict the presence of heart disease based on patient attributes such as age, cholesterol level, and resting blood pressure. This script uses two models with different architectures to classify patients into two categories: heart disease present or absent.

Command:
```bash
python heart_disease.py
```

#### Output
- Displays loss and accuracy for both models.
- Shows the classification results, including confusion matrix.

## Authors

- Marta Szpilka
- Jakub Więcek

---

This README provides an overview of the structure and usage of the scripts for image classification and heart disease prediction tasks. Each script demonstrates practical applications of neural networks for different classification problems, evaluating the models based on performance metrics such as accuracy and confusion matrices.
