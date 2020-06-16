# User settings
# - Printing information
# - Loading models

import cv2
import pygame
import tensorflow as tf
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
FPS = 30

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

# Checks / fixes
tensorflow_check = False
browser = True

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
                cv2.moveWindow(win_name, 1350, 40)
                # cv2.moveWindow(win_name, -880, 40)
            else:
                cv2.moveWindow(win_name, 1350, 40)
                # cv2.moveWindow(win_name, -880, 40)

        # Printing fps, note settings wait_key
        if display_fps:
            clock.tick(FPS)
            print(round(clock.get_fps(), 1))
        return

    # Tensorflow-gpu prints
    def check():
        if tensorflow_check:
            print("Tensorflow version:", tf.__version__)
            print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
            tf.debugging.set_log_device_placement(True)
            sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(log_device_placement=True))

            with tf.compat.v1.Session() as ses:
                # Build a graph.
                a = tf.constant(5.0)
                b = tf.constant(6.0)
                c = a * b

                # Evaluate the tensor `c`.
                print(ses.run(c))

            with tf.compat.v1.Session() as sess:
                devices = sess.list_devices()
        return
