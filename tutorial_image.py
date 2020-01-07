# youtube tutorial to train model
# video done by Tech With Tim
# https://www.youtube.com/watch?v=k-_pWoy2fb4


import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt

data = keras.datasets.fashion_mnist

(train_images, train_labels), (test_images, test_labels) = data.load_data()

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

input = train_images/255.0
test_images = test_images/255.0
output = train_labels
# input2 = input[0:, 0:1]
# input3 = np.reshape(input2, -1, 60000)


# print(train_images.shape)
# print(train_labels)
# print(train_images.shape)


# plt.imshow(test_images[2], cmap=plt.cm.binary)
# plt.xlabel("Actual: " + class_names[test_labels[2]])
# plt.show()


print(input.shape)
# print(input3.shape)
print(output.shape)
print(output)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(28, 28)),
    keras.layers.Dense(128, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
    ])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

model.fit(input, output, epochs=1)

prediction = model.predict(test_images)

print(test_labels[0])
print(np.argmax(prediction[0]))
print(prediction[0])

# for i in range(3):
    # plt.grid(False)
    # plt.imshow(test_images[i], cmap=plt.cm.binary)
    # print(test_labels[i])
    # print(prediction[i])
    # print("Prediction: " + class_names[np.argmax(prediction[i])])
    # plt.xlabel("Actual: " + class_names[test_labels[i]])
    # plt.title("Prediction: " + class_names[np.argmax(prediction[i])])

    # plt.show()
#


