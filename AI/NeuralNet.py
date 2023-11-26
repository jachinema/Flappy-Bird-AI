import random
import numpy as np


def _sign(x):
    return 1 - (2 * (x < 0))


def clamp(x, lower_bound, upper_bound):
    if x in range(lower_bound, upper_bound+1):
        return x
    elif x < lower_bound:
        return lower_bound
    return upper_bound


def mutate(matrix, mutation_rate, mutation_range):

    random_values = np.random.uniform(-mutation_range, mutation_range, matrix.shape)

    mutation_mask = np.random.rand(*matrix.shape) < mutation_rate

    mutated_matrix = matrix + random_values * mutation_mask

    return mutated_matrix


def sigmoid(x):
    #
    #
    # return 1 / (1 + np.exp(-x))
    return np.maximum(0, x)

class NeuralNet:
    def __init__(self,
                 input_size,
                 hidden_size,
                 output_size,
                 base_weights=None,
                 base_biases=None,
                 hidden_weights=None,
                 hidden_biases=None):

        if base_weights is None:
            self.base_weights = np.matrix(
                [[random.uniform(-1, 1) for __ in range(input_size)] for _ in range(hidden_size)]
            )

        else:
            self.base_weights = base_weights

        if base_biases is None:
            self.base_biases = np.matrix([[random.uniform(-10, 10)] for __ in range(hidden_size)])
        else:
            self.base_biases = base_biases

        if hidden_weights is None:
            self.hidden_weights = np.matrix([
                [random.uniform(-1, 1) for __ in range(hidden_size)] for _ in range(output_size)]
            )
        else:
            self.hidden_weights = hidden_weights

        if hidden_biases is None:
            self.hidden_biases = np.matrix([[random.uniform(-0.1, 0.1)] for __ in range(output_size)])
        else:
            self.hidden_biases = hidden_biases

    def forward(self, state):
        state = np.array(state).reshape(-1, 1)

        hidden_in = np.dot(self.base_weights, state) + self.base_biases
        hidden_out = sigmoid(hidden_in)

        output_in = np.dot(self.hidden_weights, hidden_out) + self.hidden_biases
        out = sigmoid(output_in)

        return out.flatten()

    def __call__(self, *args, **kwargs):
        return self.forward(*args, **kwargs)

