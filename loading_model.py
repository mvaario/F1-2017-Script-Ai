from tensorflow import keras
import numpy as np

class balance:

    def __init__(self):

        self.i = 20

    # Changing input shape
    def input_shape(self, input):

        x = []
        for i in range(len(input)):
            x.append([input[i], [0, 0, 0, 0, 0]])

        input = np.asarray(x)

        return input

    # Testing
    def testing_x(self, input, prediction):

        i = state.i
        for k in range(i):

            print("inputs ", input[k:k + 1, 0:1])
            print("Prediction values ", prediction[k])
            k = int(np.argmax(prediction[k]))
            print("Prediction ", k)

            if k == 3:
                k = "straight"
            elif k > 3:
                k = "Right"
            else:
                k = "left"
            print("Moves ", k)
            print("---------")
        return


    def testing_y(self, input, prediction):

        i = state.i
        for k in range(i):
            pre = prediction[k]

            l = int(np.argmax(pre))

            print(input[k])
            print(l)
            print("---------")


            gas = np.sum(pre[:3])
            zero = np.sum(pre[3:4])
            brake = np.sum(pre[4:])

            # print(gas)
            print(brake)
            all = (brake - gas) * 100
            print((all))
            print("---------")




        return



if __name__ == '__main__':
    state = balance()

    # Loading model and inputs
    model_x = keras.models.load_model("x_axis.h5")
    model_y = keras.models.load_model("y_axis.h5")
    # input = np.load('input_data.npy', allow_pickle=True)

    # Test inputs
    input = np.array([[1,0,0,0,0],[0,0,2,0,0],[0,0,0,0,3],[1,0,0,0,0],[0,0,2,0,0],[0,0,0,0,3],[1,0,0,0,0],[0,0,2,0,0],[0,0,0,0,3],[1,0,0,0,0]])

    # Input shape change
    input = state.input_shape(input)

    # x axis
    model = model_x
    prediction = model.predict(input)
    # input_data.append([x, slope, brake, old_brake, v])

    # Testing
    # state.testing_x(input, prediction)

    # y axis
    model = model_y
    prediction = model.predict(input)

    # Testing
    state.testing_y(input, prediction)







