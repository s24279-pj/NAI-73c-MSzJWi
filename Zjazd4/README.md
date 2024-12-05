# README: SVC and Decision Tree Classifiers

## Project Description

This project demonstrates the application of two different classification algorithms:
1. **SVC (Support Vector Classifier)** with an RBF (Radial Basis Function) kernel.
2. **Decision Trees**.

Both algorithms are used for classification tasks on two datasets:
- **Abalone Dataset**: Classifying the age of abalone shells based on their length and diameter.
- **Heart Disease Dataset**: Classifying the presence of heart disease based on age and cholesterol level.

## Project Structure

### Files and Scripts

- `abalone_svc.py`: SVC classifier for the Abalone dataset.
- `abalone_decision_tree.py`: Decision tree classifier for the Abalone dataset.
- `heart_disease_svc.py`: SVC classifier for the Heart Disease dataset.
- `heart_disease_decision_tree.py`: Decision tree classifier for the Heart Disease dataset.
- `utilities_hd.py`: Utility functions for visualizing decision boundaries of classifiers.
- `heart.csv`: Heart disease dataset containing features like age and cholesterol levels.
- README.md: Documentation for the project (this file).

### Datasets

1. **Abalone Dataset**: Contains information about abalone shells, including length, diameter, and the number of rings, which is used to estimate their age. This dataset is fetched from OpenML.
2. **Heart Disease Dataset**: Contains data about patients, including features like age, cholesterol levels, and whether they have heart disease. This dataset is loaded from a CSV file (`heart.csv`).

## Usage

### Requirements

To run the scripts, make sure you have the following Python packages installed:

- `numpy`
- `matplotlib`
- `pandas`
- `scikit-learn`

You can install them using `pip`:

```bash
pip install numpy matplotlib pandas scikit-learn


## Authors

Marta Szpilka
Jakub Więcek
