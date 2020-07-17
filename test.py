import numpy as np
from tensorflow import keras
import random

input = []
output = []
for i in range(50):
    x1 = random.randint(0, 10)
    x2 = random.randint(0, 10)
    x3 = random.randint(0, 10)
    x4 = random.randint(0, 10)
    x5 = random.randint(0, 10)
    x6 = random.randint(0, 10)
    x = [[x1, x2, x3, x4, x5, x6], [x1, x2, x3, x4, x5, x6]]
    input.append(x)

    if x1 > x2:
        if x1 > x3:
            move = 1
        else:
            move = 3

    elif x2 > x3:
        move = 2

    else:
        move = 3

    y = move
    output.append(y)
input = np.asarray(input)
output = np.asarray(output)

model_x = keras.Sequential([
            keras.layers.Flatten(input_shape=(2, 6)),
            keras.layers.Dense(20, activation="relu"),
            # keras.layers.Dense(40, activation="relu"),
            # keras.layers.Dense(20, activation="relu"),
            # keras.layers.Dense(14, activation="relu"),
            keras.layers.Dense(10, activation="softmax"),
        ])

model_x.compile(optimizer="adam",
                loss="sparse_categorical_crossentropy",
                metrics=["accuracy"]
                )

model_x.fit(input, output, epochs=100)


