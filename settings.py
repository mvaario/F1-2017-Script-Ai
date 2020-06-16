# User settings
# - Printing information
# - Loading models

import time
import cv2
import pygame
from tensorflow import keras

clock = pygame.time.Clock()

# Display settings
win_name = "F1 Screen"
dual_monitor = True
width = 1920
height = 1080
running = True

wait_key = 1
display = True
display_fps = True

# AI setup
ai = True
record = False
sample_rate = 20
save = False
data_balance = False
epochs = 10

# Screen position
pos_x = width / 2
pos_y = height / 2

class options:
    # Recording settings
    def ai_record():

        print("AI is True")
        # Printing recording device
        print("Recording inputs")
        pygame.display.init()
        pygame.joystick.init()
        pygame.joystick.Joystick(0).init()

        # Prints the joystick's name
        JoyName = pygame.joystick.Joystick(0).get_name()
        print("Recording device:", JoyName)
        print("Saple rate", sample_rate)

        # input data all
        input_data = []
        # turn
        output_data_x = []
        # gas / brake
        output_data_y = []

        return input_data, output_data_x, output_data_y

    # Loading models
    def ai_models():
        model_x = keras.models.load_model("x_axis.h5")
        model_y = keras.models.load_model("y_axis.h5")
        print("AI is True")
        print("Loading models")

        return model_x, model_y

    # SETUPS
    # Displaying video and FPS
    def setups(video):
        # Displaying
        if display:
            cv2.imshow(win_name, video)
            if ai and record:
                # cv2.moveWindow(win_name, 1350, 40)
                cv2.moveWindow(win_name, -880, 40)
            else:
                cv2.moveWindow(win_name, 1350, 40)
                # cv2.moveWindow(win_name, -880, 40)

        # Printing fps, note settings wait_key
        if display_fps:
            clock.tick(30)
            print(round(clock.get_fps(), 1))
        return
