import numpy as np
import matplotlib.pyplot as plt

def visualize_classifier(classifier, X, y, title=''):
    # Define the minimum and maximum values for X and Y
    # that will be used in the mesh grid
    min_x, max_x = X[:, 0].min() - 5, X[:, 0].max() + 5
    min_y, max_y = X[:, 1].min() - 20, X[:, 1].max() + 20

    # Define the step size to use in plotting the mesh grid
    mesh_step_size = 1

    # Define the mesh grid of X and Y values
    x_vals, y_vals = np.meshgrid(np.arange(min_x, max_x, mesh_step_size), np.arange(min_y, max_y, mesh_step_size))

    # Run the classifier on the mesh grid
    output = classifier.predict(np.c_[x_vals.ravel(), y_vals.ravel()])

    # Reshape the output array
    output = output.reshape(x_vals.shape)

    # Create a plot
    plt.figure()

    # Specify the title
    plt.title(title)

    # Choose a color scheme for the plot
    plt.pcolormesh(x_vals, y_vals, output, cmap=plt.cm.Paired)

    # Overlay the training points on the plot
    scatter = plt.scatter(X[:, 0], X[:, 1], c=y, s=75, edgecolors='black', linewidth=1, cmap=plt.cm.Paired)

    legend_labels = ['Healthy', 'Diseased']  # Odpowiednie etykiety dla wartości 0 i 1
    handles, labels = scatter.legend_elements()
    plt.legend(handles, legend_labels, title="Condition")

    plt.xlabel('Age')
    plt.ylabel('Cholesterol')
    # Specify the boundaries of the plot
    plt.xlim(x_vals.min(), x_vals.max())
    plt.ylim(y_vals.min(), y_vals.max())

    # Specify the ticks on the X and Y axes
    plt.xticks((np.arange(int(X[:, 0].min() - 5), int(X[:, 0].max() + 5), 5)))
    plt.yticks((np.arange(int(X[:, 1].min() - 20), int(X[:, 1].max() + 20), 100)))

    plt.show()
