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

        # Making testing data
        input_x_test, output_x_test = balance.testing_data(input_x, output_x)

        # Changing len
        # input_x, output_x = balance.axis_len(input_x, output_x)

        # Output change
        output_x = balance.output_change(output_x)
        output_x_test = balance.output_change(output_x_test)

        # shuffle
        input_x, output_x = balance.shuffle(input_x, output_x)

        output_x = output_x.reshape(-1)
        output_x_test = output_x_test.reshape(-1)

        return input_x, output_x, input_x_test, output_x_test

    # Y axis balance and shuffle
    def y_axis(input_y, output_y):

        # shuffle
        input_y, output_y = balance.shuffle(input_y, output_y)

        # Making testing data
        input_y_test, output_y_test = balance.testing_data(input_y, output_y)

        # Changing len
        # input_y, output_y = balance.axis_len(input_y, output_y)

        # Output change
        output_y = balance.output_change(output_y)
        output_y_test = balance.output_change(output_y_test)

        # Shuffle
        input_y, output_y = balance.shuffle(input_y, output_y)

        output_y = output_y.reshape(-1)
        output_y_test = output_y_test.reshape(-1)

        return input_y, output_y, input_y_test, output_y_test

    # Making testing data
    def testing_data(input, output):
        input_test = []
        output_test = []
        for i in range(test_size):
            num = random.randint(1, len(input)-1)
            input_test.append(input[num])
            output_test.append(output[num])

        input_test = np.asarray(input_test)
        output_test = np.asarray(output_test)

        return input_test, output_test

    # Changing data lens
    def axis_len(input, output):
        data = []
        for i in range(len(input)):
            data.append([input[i], output[i]])

        data = np.asarray(data)

        left = []
        right = []
        straight = []
        for i in range(len(data)):
            row = data[i]
            input_data = row[0]
            output_data = row[1]

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

        input = input.reshape(-1, 2, 6)
        output = output.reshape(-1, 3)

        return input, output

    # Changing output data
    def output_change(output):
        output_final = []
        for i in range(len(output)):
            output_data = output[i]

            if output_data[0] > 0:
                data = output_data[0]
                if data > 0.8:
                    move = 5
                elif data > 0.6:
                    move = 4
                elif data > 0.4:
                    move = 3
                elif data > 0.2:
                    move = 2
                else:
                    move = 1

            elif output_data[2] > 0:
                data = output_data[2]
                if data > 0.8:
                    move = 10
                elif data > 0.6:
                    move = 9
                elif data > 0.4:
                    move = 8
                elif data > 0.2:
                    move = 7
                else:
                    move = 6

            elif output_data[1] > 0:
                move = 0


            else:
                print("error", output[i])
                print("line", i)
                quit()


            output_final.append([move])


        output = np.asarray(output_final)

        return output

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
            keras.layers.Flatten(input_shape=(2, 6)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(88, activation="relu"),
            keras.layers.Dense(44, activation="relu"),
            keras.layers.Dense(22, activation="relu"),
            keras.layers.Dense(11, activation="softmax"),
        ])

        model_x.compile(optimizer="adam",
                        loss="sparse_categorical_crossentropy",
                        metrics=["accuracy"]
                        )

        return model_x

    # Building Y-axis model
    def model_y(input_y):
        model_y = keras.Sequential([
            keras.layers.Flatten(input_shape=(2, 6)),
            keras.layers.Dense(128, activation="relu"),
            keras.layers.Dense(88, activation="relu"),
            keras.layers.Dense(44, activation="relu"),
            keras.layers.Dense(22, activation="relu"),
            keras.layers.Dense(11, activation="softmax"),
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


            tensorboard = TensorBoard(log_dir="logs\\{}".format(time()))
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

    # Testing models
    def model_testing(model_x, model_y, input_x_test, output_x_test, input_y_test, output_y_test):
        x = model_x.predict(input_x_test)
        y = model_y.predict(input_y_test)

        miss_x = 0
        miss_y = 0
        for i in range(len(input_x_test)):
            x1 = np.argmax(x[i])
            x2 = np.argmax(output_x_test[i])
            if x1 != x2:
                miss_x = miss_x + 1

        for i in range(len(input_y_test)):
            y1 = np.argmax(y[i])
            y2 = np.argmax(output_y_test[i])
            if y1 != y2:
                miss_y = miss_y + 1

        print("--------------------")
        print("x-axis accurate:", round(1 - miss_x / len(input_x_test), 4))
        print("y-axis accurate:", round(1 - miss_y / len(input_y_test), 5))
        print("")
        print("Examples:")

        for i in range(5):
            num = random.randint(1, len(input_x_test)-1)
            print("Prediction:", np.argmax(x[num]), "Actual:", np.argmax(output_x_test[num]))



        return
