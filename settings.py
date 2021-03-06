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
display_fps = False
FPS = 30
joynum = 1
wheel = True

# AI settings
ai = True
record = False
sample_rate = 500
save = False
data_balance = False
epochs = 100
test_size = 1000

# Screen position
pos_x_min = int(width / 2 - 535)
pos_x_max = int(width / 2 + 535)
pos_y_min = int(height / 2 - 80)
pos_y_max = int(height / 2 + 410)

# Resize
k = 0.5
size_x = int((pos_x_max - pos_x_min) * k)
size_y = int((pos_y_max - pos_y_min) * k)

# Checks / fixes
tensorflow_check = False
browser = True

class options:
    # Recording settings
    def ai_record():
        try:
            # Printing recording device
            print("Recording inputs")
            pygame.display.init()
            pygame.joystick.init()
            pygame.joystick.Joystick(joynum).init()

            # Prints the joystick's name
            JoyName = pygame.joystick.Joystick(joynum).get_name()
            print("Recording device:", JoyName)
            print("Sample rate:", sample_rate)
            print("Save:", save)

            # input data all
            input_data = []
            # turn
            output_data_x = []
            # gas / brake
            output_data_y = []
        except:
            print("No joystick found", joynum)
            print("Change joy number")
            quit()

        return input_data, output_data_x, output_data_y

    # Loading models
    def ai_models():
        model_x = keras.models.load_model("x_axis.h5")
        model_y = keras.models.load_model("y_axis.h5")
        print("AI:", ai)
        print("Loading models")

        return model_x, model_y

    # SETUPS
    # Displaying video and FPS
    def setups(video):
        # Displaying
        if display:
            cv2.imshow(win_name, video)
            if ai and record:
                cv2.moveWindow(win_name, int(-width), 40)
            else:
                cv2.moveWindow(win_name, int(width-size_x), 40)

        # Printing fps, note settings wait_key
        clock.tick(FPS)
        if display_fps:
            print(round(clock.get_fps(), 1))
        return

    # Tensorflow-gpu prints
    def check():
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
