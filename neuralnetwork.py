import numpy as np
from scipy.special import expit


class NeuralNetwork():
    """
        NOTE: Currently supports only 1 hidden layer.
        layers = (x, y, z)
        Defines a neural network -> x input | y hidden | z outputs
    """

    def __init__(self, layers, learn_rate=0.3):
        self.layers = layers
        self.learning_rate = learn_rate
        self.whi = np.random.normal(0.0,
                                    pow(self.layers[0], -0.5),
                                    tuple(reversed(self.layers[0:2])))
        self.who = np.random.normal(0.0,
                                    pow(self.layers[1], -0.5),
                                    self.layers[2:0:-1])

    def train(self, input_list, target_list):
        inputs = np.array(input_list, ndmin=2).T
        targets = np.array(target_list, ndmin=2).T

        hidden_inps = np.matmul(self.whi, inputs)
        hidden_outs = self.activation(hidden_inps)

        final_inputs = np.matmul(self.who, hidden_outs)
        final_outs = self.activation(final_inputs)

        output_errors = targets - final_outs
        hidden_errors = np.matmul(self.who.T, output_errors)

        # j-k lr * E * activation(Ok) * (1 - activation(Ok)) dot Transpose(Oj)
        self.who += self.learning_rate * \
            np.matmul((output_errors * final_outs * (1.0 - final_outs)),
                      np.transpose(hidden_outs))
        self.whi += self.learning_rate * \
            np.matmul((hidden_errors * hidden_outs * (1.0 - hidden_outs)),
                      np.transpose(inputs))

    def query(self, input_list):
        # Converts list to matrix
        inputs = np.array(input_list, ndmin=2).T

        hidden_inps = np.matmul(self.whi, inputs)
        hidden_outs = self.activation(hidden_inps)

        final_inputs = np.matmul(self.who, hidden_outs)
        final_outs = self.activation(final_inputs)

        return final_outs

    def query_with_weights(self, input_list, weights):
        # Converts list to matrix
        wi = weights[0]
        wo = weights[1]
        inputs = np.array(input_list, ndmin=2).T

        hidden_inps = np.matmul(wi, inputs)
        hidden_outs = self.activation(hidden_inps)

        final_inputs = np.matmul(wo, hidden_outs)
        final_outs = self.activation(final_inputs)

        return final_outs

    # NOTE: Using Sigmoid
    def activation(self, x):
        return expit(x)
