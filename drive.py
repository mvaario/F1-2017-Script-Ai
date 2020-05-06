import pyvjoy
from main import *
from settings import *


vjoy = pyvjoy.VJoyDevice(1)

# Script drive
class script:

    def start(self):
        script.turn(self)
        script.speed(self)
        vjoy.update()
        return

    # Changing virtual controller x-axis
    def turn(self):

        x = self.x
        slope = self.slope * 2
        speed = self.v

        ss = slope / 20 + speed
        if ss == 0:
            ss = 1

        x = 16400 + x * 41 / ss

        x = int(x)
        vjoy.data.wAxisX = 0x0 + x

        return

    # Changing virtual controller y-axis
    def speed(self):

        # GAS
        ag = self.ag
        v = self.v
        slope = self.slope
        x = abs(self.x)

        # prosentit!
        x = (x / 200) * 8200
        slope = (1.1 - slope / 50) * 8200
        ag = (100 - ag) * 25
        v = 7500 - 1 / v * 10000

        y = x + slope + v + ag
        if y > 16400:
            y = 16400

        # BRAKE
        c = script.brake(self)
        if c != 0:
            y = c

        y = int(y)
        vjoy.data.wAxisY = 0x0 + y
        return

    # Checking if braking_force != 0, changing virtual controller y-axis
    def brake(self):
        b = self.brake
        o_b = self.old_brake

        ag = self.ag
        v = self.v
        slope = self.slope
        x = abs(self.x)
        c = 0

        if b != 0:
            b = 20
            o_b = 20
        if b > 20:
            b = 20
        if o_b > 20:
            o_b = 20

        # Prosentit
        b = 0.05 * b * 8200
        o_b = 0.05 * o_b * 8200

        c = 16400 + b + o_b
        return c

# Recording inputs
class ai_record:

    # Saving inputs and outputs
    def model_record(self, input_data, output_data_x, output_data_y):
        pygame.event.pump()

        x = self.x
        slope = self.slope
        v = self.v
        b = self.brake
        o_b = self.old_brake

        # Inputs
        input_data.append([x, slope, b, o_b, v])

        # Turn record
        left, straight, right = ai_record.x_position()
        output_data_x.append([left, straight, right])

        # Gas/Braking record
        gas, zero, brake = ai_record.y_position()
        output_data_y.append([gas, zero, brake])

        # Saving data
        if len(input_data) % sample_rate == 0:
            print("Frames", len(input_data))
            if save is True:
                np.save("input_data", input_data)
                np.save("output_x", output_data_x)
                np.save("output_y", output_data_y)
        return

    # Getting X-axis info (Turing keys)
    def x_position():

        # Prints the values for axis0-4
        axis = float(pygame.joystick.Joystick(0).get_axis(0))
        # -1 to 1
        left = [0]
        straight = [0]
        right = [0]

        if axis < -0.006:
            if axis < -0.99:
                axis = -1
            left = [abs(axis)]

        elif axis > 0.006:
            if axis > 0.99:
                axis = 1
            right = [axis]
        else:
            straight = [1]

        return left, straight, right

    # Getting Y-axis info (Gas / braking axis)
    def y_position():

        # Values for axis0-4
        gas = [0]
        zero = [0]
        brake = [0]

        # Gas 1 to -1
        gas = float(pygame.joystick.Joystick(0).get_axis(2))
        gas = (gas - 1) / -2
        if gas > 0.999:
            gas = 1
        if gas < 0.005:
            gas = 0

        # Braking
        brake = float(pygame.joystick.Joystick(0).get_axis(3))
        brake = (1 - brake) / 2
        if brake > 0.999:
            brake = 1
        if brake < 0.005:
            brake = 0

        if gas == 0 and brake == 0:
            zero = 1

        return gas, zero, brake


class ai_drive:
    # Driving with trained model
    def model_drive(self, model_x, model_y):

        # Input shape change
        input = ai_drive.input_shape(self)

        # Prediction x-axis
        x = ai_drive.model_turn(model_x, input)

        # Prediction y-axis
        y = ai_drive.model_gas(self, model_y, input)

        ai_drive.controller(x, y)

        return

    # Changing input data
    def input_shape(self):
        x = self.x
        slope = self.slope
        v = self.v
        b = self.brake
        o_b = self.old_brake

        # Inputs
        input = []
        input.append([x, slope, b, o_b, v])

        x = []
        for i in range(len(input)):
            x.append([input[i], [0, 0, 0, 0, 0]])

        input = np.asarray(x)

        return input

    # Getting turning percent
    def model_turn(model_x, input):

        model = model_x
        prediction = model.predict(input)

        left = np.sum(prediction[0:, :3])
        right = np.sum(prediction[0:, 4:])

        x = right - left
        return x

    # Getting gas percent
    def model_gas(self, model_y, input):

        model = model_y
        prediction = model.predict(input)

        gas = np.sum(prediction[0:, :3])
        brake = np.sum(prediction[0:, 4:])

        # if self.brake == 0 and self.old_brake == 0:
        #     brake = 0
        # else:
        #     gas = 0

        y = brake - gas
        return y

    # Updating controller
    def controller(x, y):

        # turn
        x = 16400 + (16400 * x)
        x = int(x)
        vjoy.data.wAxisX = 0x0 + x

        # gas
        y = 16400 + (16400 * y)
        y = int(y)
        vjoy.data.wAxisY = 0x0 + y

        vjoy.update()
        return
