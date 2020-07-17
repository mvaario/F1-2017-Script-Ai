# Everything for driving and sending inputs
# - Calculating script keys
# - Recording AI models
# - AI predictions
# - Sending AI predictions to joystick
# made by mvaario

import pyvjoy
import numpy as np
from main import *
from settings import *
import random

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
        v = self.v

        ss = slope / 20 + v
        if ss == 0:
            ss = 1

        x = x * 2

        x = 16400 + x * 41 / ss

        x = int(x)
        vjoy.data.wAxisX = 0x0 + x

        return

    # Changing virtual controller y-axis
    def speed(self):

        # GAS
        v = self.v
        slope = self.slope
        x = abs(self.x)

        # Script calibrations
        x = x * 50
        slope = slope * 100
        v = v * 100

        y = x + slope + v + 7500
        if y > 16400:
            y = 16400

        # BRAKE
        c = script.brake(self)
        if c > 16400:
            y = c - y*2

        y = int(y)
        vjoy.data.wAxisY = 0x0 + y
        return

    # Checking if braking_force != 0, changing virtual controller y-axis
    def brake(self):
        b = self.brake
        o_b = self.old_brake

        if b > 20:
            b = 20
        if o_b > 20:
            o_b = 20

        # Prosentit
        b = 0.05 * b * 8200
        o_b = 0.05 * o_b * 8200

        c = b + o_b + 16400
        return c

# Recording inputs
class ai_record:

    # Saving inputs and outputs
    def model_record(self, input_data, output_data_x, output_data_y):
        pygame.event.pump()

        x = self.x / (size_x*0.37383)
        slope = self.slope / 20
        v = self.v / 2
        b = self.brake / 10
        o_b = self.old_brake / 10
        side = self.side / (size_x*0.0374)
        line = self.line

        # Recording inputs
        input_data.append([[x, slope, b, o_b, side, v], line])
        self.line = [x, slope, b, o_b, side, v]

        # Recording x-axis
        left, straight, right = ai_record.x_position()
        # print(left, straight, right)
        output_data_x.append([left, straight, right])

        # Recording y_axis
        gas, zero, brake = ai_record.y_position()
        output_data_y.append([gas, zero, brake])
        # print(gas, zero, brake)

        # Saving data
        if save is True and len(input_data) % sample_rate == 0:
            print("Saved frames", len(input_data))
            np.save("input_data", input_data)
            np.save("output_x", output_data_x)
            np.save("output_y", output_data_y)
        elif len(input_data) % sample_rate == 0:
            print("Frames", len(input_data))
        return

    # Getting X-axis info (Turing keys)
    def x_position():
        # Prints the values for axis0-4
        left = 0
        straight = 0
        right = 0
        if wheel:
            axis = float(pygame.joystick.Joystick(joynum).get_axis(0))
        else:
            axis = float(pygame.joystick.Joystick(joynum).get_axis(4))
        if -0.1 < axis < 0.1:
            straight = 1
        elif axis < -0.1:
            if axis < -0.99:
                left = 1
            else:
                left = abs(axis)
        elif axis > 0.1:
            if axis > 0.99:
                right = 1
            else:
                right = axis
        else:
            print("Error axis value", axis)

        return left, straight, right

    # Getting Y-axis info (Gas / braking axis)
    def y_position():
        # Values for axis0-4
        # Gas 1 to -1
        brake = 0
        gas = 0
        zero = 0

        axis = float(pygame.joystick.Joystick(joynum).get_axis(2))
        axis = (1 - axis) / 2

        if axis > 0.1:
            if axis > 0.99:
                gas = 1
            else:
                gas = axis

        axis = float(pygame.joystick.Joystick(joynum).get_axis(3))
        axis = (1 - axis) / 2
        if axis > 0.1:
            if axis > 0.99:
                brake = 1
            else:
                brake = axis

        if gas == 0 and brake == 0:
            zero = 1

        return gas, zero, brake

class ai_drive:
    # Driving with trained model
    def model_drive(self, model_x, model_y):

        # Getting input
        input = ai_drive.input_shape(self)



        # Prediction
        x, y = ai_drive.prediction(self, input, model_x, model_y)

        # Sending inputs to controller
        ai_drive.controller(x, y)

        return

    # Changing input data
    def input_shape(self):
        x = self.x / (size_x*0.37383)
        slope = self.slope / 20
        v = self.v / 2
        b = self.brake / 10
        o_b = self.old_brake / 10
        side = self.side / (size_x*0.0374)
        line = self.line

        input = []
        input.append([[x, slope, b, o_b, side, v], line])
        self.line = [x, slope, b, o_b, side, v]
        input = np.asarray(input)

        return input

    # Prediction
    def prediction(self, input, model_x, model_y):

        # X-axis
        x = model_x(input, training=False)
        left = np.sum(x[0:, :3])
        right = np.sum(x[0:, 4:])
        x = right - left
        print(right)
        print(left)

        # Y-axis
        y = model_y(input, training=False)

        gas = np.sum(y[0:, :3])
        if self.v != 1 and self.brake != 0:
            brake = np.sum(y[0:, 4:])
        else:
            brake = 0
        y = brake - gas

        return x, y

    # Updating controller
    def controller(x, y):
        # X-axis
        x = 16384 + (16384 * x)
        x = int(x)
        vjoy.data.wAxisX = 0x0 + x

        # Y-axis
        y = 16384 + (16384 * y)
        y = int(y)
        vjoy.data.wAxisY = 0x0 + y

        vjoy.update()
        return
