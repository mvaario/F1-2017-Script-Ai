# Changing virtual joystick
# Using pygame and Vjoy to emulate virtual joystick
# made by mvaario

import pyvjoy
import pygame
import numpy as np

# Calculating joystick positions
class keys:


    # SCRIPT
    # Calculating turning force
    def turn(x, slope, v):
        # Getting pyvjoy device
        vjoy = pyvjoy.VJoyDevice(1)

        # Calculating turning force
        slope = slope * 2
        ss = slope / 10 + v

        x = 16400 + x * 100 / ss

        # Sending turing to virtual joystick
        x = int(x)
        vjoy.data.wAxisX = 0x0 + x

        return vjoy

    # Calculating gas force
    def gas(x, slope, v):
        # GAS
        x = abs(x)

        # Calculating percentage
        x = (x / 200) * 8200
        slope = (1.1 - slope / 10) * 8200
        v = 7500 - 1 / v * 10000

        # Defining y
        y = x + slope + v
        if y > 16400:
            y = 16400

        return y

    # Calculating braking force
    def brake(brake, old_brake):
        # BRAKE
        # Checking how many braking lines were found
        if brake != 0 and old_brake == 0:
            old_brake = brake
        if brake > 20:
            brake = 20
        if old_brake > 20:
            old_brake = 20

        # Calculating braking force
        brake = brake * 2
        old_brake = old_brake * 1.5
        # Percentages
        brake = 0.025 * brake * 8200
        old_brake = 0.0333 * old_brake * 8200

        # Defining y
        y = 16400 + brake + old_brake + 5000




        return y

# --------------------------------------------------------

    # AI recording
    # Getting X-axis info (turning force)
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

    # Getting Y-axis info (gas/brake)
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

# --------------------------------------------------------

    # AI driving
    # Turning prediction / percentages
    def model_turn(model_x, input):

        model = model_x
        prediction = model.predict(input)

        left = np.sum(prediction[0:, :3])
        right = np.sum(prediction[0:, 4:])
        # print(left)
        x_axis = right - left

        return x_axis

    # Gas / brake prediction / percentage
    def model_gas(model_y, input, brake, old_brake):

        model = model_y
        prediction = model.predict(input)

        # Making sure fail braking
        if brake == 0 and old_brake == 0:
            brake = 0
        else:
            brake = np.sum(prediction[0:, 4:])

        gas = np.sum(prediction[0:, :3])


        y_axis = brake - gas

        return y_axis

    def model_update(x_axis, y_axis):
        # Getting pyvjoy device
        vjoy = pyvjoy.VJoyDevice(1)

        # Turning
        x = 16400 + (16400 * x_axis)
        x = int(x)
        vjoy.data.wAxisX = 0x0 + x




        # Gas / brake
        y = 16400 + (16400 * y_axis)
        y = int(y)
        vjoy.data.wAxisY = 0x0 + y

        vjoy.update()

        return



