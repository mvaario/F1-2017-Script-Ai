# Data balancing and AI training
# - Loading recorded data
# - Balancing recorded data to same length and shuffling data
# - Changing output values from [3] to [7]
# - Training model with balanced data, inputs / outputs
# made by mvaario

import random
import webbrowser
from settings import *
from tensorflow import keras
import numpy as np
from time import time
from tensorflow.python.keras.callbacks import TensorBoard

# AI data balancing
class balance:

    # X axis balance and shuffle
    def x_axis(input_x, output_x):

        # shuffle
        input_x, output_x = balance.shuffle(input_x, output_x)

        # Changing len
        # input_x, output_x = balance.axis_len(input_x, output_x)

        # Changin shape
        input_x = balance.input_shape(input_x)

        # Output change
        output_x = balance.output_change(output_x)

        # shuffle
        input_x, output_x = balance.shuffle(input_x, output_x)

        output_x = output_x.reshape(-1)

        return input_x, output_x

    # Y axis balance and shuffle
    def y_axis(input_y, output_y):

        # shuffle
        input_y, output_y = balance.shuffle(input_y, output_y)

        # Changing len
        # input_y, output_y = balance.axis_len(input_y, output_y)

        # Changing shape
        input_y = balance.input_shape(input_y)

        # Output change
        output_y = balance.output_change(output_y)

        # Shuffle
        input_y, output_y = balance.shuffle(input_y, output_y)

        output_y = output_y.reshape(-1)

        return input_y, output_y

    # Changing data lens
    def axis_len(input, output):

        data = []
        for i in range(len(input)):
            data.append([input[i], output[i]])

        data = np.asarray(data)
        data = np.reshape(data, (-1, 2))

        left = []
        right = []
        straight = []
        for i in range(len(data)):
            output_data = data[i, 1]
            input_data = data[i, 0]

            if output_data[0] != 0:
                left.append([input_data, output_data])

            elif output_data[2] != 0:
                right.append([input_data, output_data])
            else:
                straight.append([input_data, output_data])

        left = np.asarray(left)
        right = np.asarray(right)
        straight = np.asarray(straight)

        left = np.reshape(left, (-1, 2))
        right = np.reshape(right, (-1, 2))
        straight = np.reshape(straight, (-1, 2))

        straight = straight[:len(left)][:len(right)]
        left = left[:len(straight)]
        right = right[:len(straight)]

        data = np.array([left, straight, right])
        data = np.reshape(data, (-1, 2))

        input_final = []
        output_final = []
        for i in range(len(data)):
            data_final = data[i]
            input_final.append(data_final[0])
            output_final.append(data_final[1])

        input = np.asarray(input_final)
        output = np.asarray(output_final)
        input = input.reshape(-1, 5)
        output = output.reshape(-1, 3)

        return input, output

    # Changing output data from [x, 3] to [x, 7]
    def output_change(output):
        output_final = []
        for i in range(len(output)):
            output_data = output[i]

            if output_data[0] > 0.666:
                move = 0
            elif output_data[0] > 0.333:
                move = 1
            elif output_data[0] > 0:
                move = 2
            elif output_data[2] > 0.666:
                move = 4
            elif output_data[2] > 0.333:
                move = 5
            elif output_data[2] > 0:
                move = 6
            else:
                move = 3
            output_final.append([move])

        output = np.asarray(output_final)

        return output

    # Changing input shape
    def input_shape(input):
        x = []
        for i in range(len(input)):
            x.append([input[i], [0, 0, 0, 0, 0]])
        input = np.asarray(x)

        return input

    # Shuffle data
    def shuffle(input, output):
        # Shuffle data

        indices = np.arange(input.shape[0])
        np.random.shuffle(indices)
        input = input[indices]
        output = output[indices]

        return input, output


# AI training
class training:

    # Building X-axis model
    def model_x(input_x):
        model_x = keras.Sequential([
            keras.layers.Flatten(input_shape=(2, 5)),
            keras.layers.Dense(20, activation="relu"),
            keras.layers.Dense(40, activation="relu"),
            keras.layers.Dense(20, activation="relu"),
            keras.layers.Dense(14, activation="relu"),
            keras.layers.Dense(7, activation="softmax"),
        ])

        model_x.compile(optimizer="adam",
                        loss="sparse_categorical_crossentropy",
                        metrics=["accuracy"]
                        )

        return model_x

    # Building Y-axis model
    def model_y(input_y):
        model_y = keras.Sequential([
            keras.layers.Flatten(input_shape=(2, 5)),
            keras.layers.Dense(20, activation="relu"),
            keras.layers.Dense(40, activation="relu"),
            keras.layers.Dense(20, activation="relu"),
            keras.layers.Dense(14, activation="relu"),
            keras.layers.Dense(7, activation="softmax"),
        ])

        model_y.compile(optimizer="adam",
                        loss="sparse_categorical_crossentropy",
                        metrics=["accuracy"]
                        )
        return model_y

    # Fitting models
    def model_fitting(model_x, model_y, input_x, input_y, output_x, output_y):
        if browser:
            webbrowser.open('http://localhost:6006/ ', new=1)
            # for check terminal: "tensorboard --logdir=logs/
            tensorboard = TensorBoard(log_dir="logs\\{}".format(time()))

            print("Fitting X-axis")
            model_x.fit(input_x, output_x, epochs=epochs, callbacks=[tensorboard])

            print("Fitting Y-axis")
            model_y.fit(input_y, output_y, epochs=epochs, callbacks=[tensorboard])

        else:
            print("Fitting X-axis")
            model_x.fit(input_x, output_x, epochs=epochs)
            print("------------------------------------------")
            print("")
            print("Fitting Y-axis")
            model_y.fit(input_y, output_y, epochs=epochs)


        print("model_x summary")
        model_x.summary()
        print("")
        print("model_y summary")
        model_y.summary()

        if save is True:
            model_x.save("x_axis.h5")
            model_y.save("y_axis.h5")
        return
