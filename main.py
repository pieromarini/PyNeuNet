import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.misc
from neuralnetwork import NeuralNetwork

layers = (784, 200, 10)
epochs = 2
learning_rate = 0.2
network_score = []

n = NeuralNetwork(layers, learning_rate)


def mnist_train():
    with open('./mnist_train.csv', 'r') as f:
        traning_data = f.readlines()

        print("Starting Training...")
        for i in range(epochs):
            print("Epoch:", i)
            c = 0
            for record in traning_data:
                all_values = record.split(',')
                inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01

                # Show current image being tested.
                # inputs_shaped = np.asfarray(all_values[1:]).reshape((28, 28))
                # plt.imshow(inputs_shaped, cmap='Greys', interpolation='None')
                # if c < 3:
                #    plt.imsave('test{}.png'.format(
                #        c), inputs_shaped, cmap='Greys')
                #    c += 1

                # Creates the desired output layer based on
                # the amount of output nodes used in the network.
                targets = np.zeros(layers[-1]) + 0.01
                targets[int(all_values[0])] = 0.99
                n.train(inputs, targets)


def mnist_test():
    with open('./mnist_test.csv', 'r') as f:
        test_data = f.readlines()
        for record in test_data:
            all_values = record.split(',')
            correct_label = int(all_values[0])
            inputs = (np.asfarray(all_values[1:]) / 255.0 * 0.99) + 0.01
            outputs = n.query(inputs)
            label = np.argmax(outputs)

            if label == correct_label:
                network_score.append(1)
            else:
                network_score.append(0)

            # print("Correct:", correct_label, "| Answer:", label)


def pre_process_custom_image(path):
    """
        Extracts the label from the image path '*_1.png'.
        Reads and flattens the pixels into an array and grayscales the image.
        Reshapes the array into 784 pixels and normalizes them between 0.1-1
    """
    label = int(path[-5:-4])
    img_flat = scipy.misc.imread(path, flatten=True)
    img_data = 255.0 - img_flat.reshape(784)
    img_data = (img_data / 255.0 * 0.99) + 0.01
    return (label, img_data)


def test_custom_image(path):
    correct_label, img_data = pre_process_custom_image(path)
    # Show current image being tested.
    img_data_shaped = img_data.reshape((28, 28))
    plt.imshow(img_data_shaped, cmap='Greys', interpolation='None')
    plt.show()
    outputs = n.query(img_data)
    label = np.argmax(outputs)

    if label == correct_label:
        network_score.append(1)
    else:
        network_score.append(0)

    print("Correct Label:", correct_label, "| Answer:", label)


mnist_train()
mnist_test()
base = './test-images/'
files = os.listdir(base)
for f in files:
    test_custom_image(base + f)

# Print overall Network performance
score = np.asarray(network_score)
print("Performance:", score.sum() / score.size)
