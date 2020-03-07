# Game F1 2017, intent to make self-driving script / ai
# Taking ss from game window and finding the best line
# Recording Controller / Wheel positions
# Recording Gas / Brake
# Recording best line position (x-pos, y-pos and slope), added recording speed
# Saving inputs (best line position) and outputs (wheel position and gas), input_data.npy, output_x.npy and output_y.npy
# Added script to drive without Ai training (self.ai = 0)
# made by mvaario

from settings import *
from sprites import *
from keys import *
from line_calculations import *
from grabscreen import grab_screen
import time
from getkeys import key_check
import cv2
import numpy as np
import pygame as pg
import pyvjoy

class main:
    def __init__(self):
        self.clock = pg.time.Clock()

        # x/y-axis average
        self.x = 0
        self.y = 0
        self.slope = 0

        # Braking
        self.brake = 0
        self.old_brake = 0

        # speed
        self.v = 1

        return

    # Start / Recording game window
    def start(self):
        # Taking screen shot from game window
        video = main.grab_screen()
        # Resizing the window
        video = cv2.resize(video, (851, 349))
        # Making copy of the window
        video_copy = np.copy(video)

        return video, video_copy

    # Record game window
    def grab_screen(self):

        global video
        # If user is using dual monitor setup
        if dual_monitor:
            # Checking ai from settings
            if ai and ai_record:
                video = grab_screen(region=(width, height, width + 1180, height + 349))
            else:
                video = grab_screen(region=(-1700, 400, -850, 770))
            # Converting colors BGR to RGB
            video = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
        return video

    # Finding turning, braking lines and speed
    def finding_lines(self, video, video_copy):
        x = main.x
        y = main.y
        v = main.v

        # TURN
        # Region to find green pixels
        region = bestline.region_of_interest_turn(video, video_copy, x)
        # Finding green pixels
        green_pixels = bestline.green_pixels(region)

        # BRAKE
        # Region to find red pixels
        region = brakeline.region_of_interest_brake(video, video_copy, x, y, v)
        # Finding red pixels
        red_pixels = brakeline.red_pixels(region)

        #   SPEED
        # Finding speed meter position
        region = speedometer.region_of_interest_speed(video, video_copy)
        # Finding white pixels
        v = speedometer.white_pixels(region)
        main.v = v

        # Drawing lines
        lines = main.drawing_lines(video, green_pixels, red_pixels)

        return lines

    # Line Drawing
    def drawing_lines(self, video, green_pixels, red_pixels):
        old_brake = main.old_brake
        v = main.v
        x = main.x
        slope = main.slope

        # Drawing lines using green pixels
        video, lines = drawing.bestline(video, green_pixels)

        # Drawing lines using red pixels
        braking, old_brake = drawing.brakeline(video, red_pixels, x, v, slope, old_brake)

        # Saving braking
        main.brake = braking
        main.old_brake = old_brake

        return lines

    # Calculations
    def line_calculations(self, lines):
        x = main.x
        y = main.y
        slope = main.slope

        # Average turning line
        x, y = calculations.average_line(video, lines, x, y)
        # Average slope
        slope = calculations.slope(x, y, slope)

        # Saving x, y and slope
        main.x = x
        main.y = y
        main.slope = slope
        return

    # Define driving mode
    def driving_mode(self):
        if not ai and not ai_record:
            # Running the script keys
            main.script()
        elif ai and ai_record:
            # Recording data
            main.record()
        else:
            # Model drive
            main.ai_drive()

        return

    # Keys
    def script(self):
        x = main.x
        slope = main.slope
        v = main.v
        brake = main.brake
        old_brake = main.old_brake

        # Changing x-axis
        vjoy = keys.turn(x, slope, v)

        # If braking lines were found
        if brake != 0 or old_brake != 0:
            y = keys.brake(brake, old_brake)
        else:
            # Changing y-axis
            y = keys.gas(x, slope, v)

        # Sending turing to virtual joystick
        y = int(y)
        vjoy.data.wAxisY = 0x0 + y

        # Updating vjoy
        vjoy.update()
        return

    # TENSORFLOW
    # Recording data
    def record(self):
        pygame.event.pump()
        x = main.x
        slope = main.slope
        v = main.v
        brake = main.brake
        old_brake = main.old_brake

        # Getting info from screen
        input_data.append([x, slope, brake, old_brake, v])

        # Getting users turning info
        left, straight, right = keys.x_position()
        output_data_x.append([left, straight, right])

        # Getting users gas/brake info
        gas, zero, brake = keys.y_position()
        output_data_y.append([gas, zero, brake])

        # Saving data
        if len(input_data) % sample_rate == 0:
            print("Frames", len(input_data))
            if save:
                np.save("input_data", input_data)
                np.save("output_x", output_data_x)
                np.save("output_y", output_data_y)

        return

    # models driving
    def ai_drive(self):
        x = main.x
        slope = main.slope
        v = main.v
        brake = main.brake
        old_brake = main.old_brake

        # Changing input shape
        input = ai.input_shape(x, slope, v, brake, old_brake)

        # Predicting x-axis
        x_axis = keys.model_turn(model_x, input)

        # Predicting y-axis
        y_axis = keys.model_gas(model_y, input, brake, old_brake)

        # Sending predictions to joystick
        keys.model_update(x_axis, y_axis)

        return



    # SETUPS
    # Displaying video and FPS
    def setups(self, last_time):
        # Locking FPS
        main.clock.tick(FPS)
        # Displaying
        if display:
            cv2.imshow(win_name, video)
            if ai and ai_record:
                cv2.moveWindow(win_name, -880, 40)
                wait_key = 1
            else:
                # cv2.moveWindow(win_name, 1055, 40)
                cv2.moveWindow(win_name, -880, 40)
                wait_key = 1

        # Printing fps, note waitkey
        if display_fps:
            print(round(1 / (time.time() - last_time)))
            last_time = time.time()

        return wait_key, last_time


if __name__ == '__main__':

    print("")
    main = main()
    pg.init()
    last_time = time.time()
    check_key = key_check()
    vjoy = pyvjoy.VJoyDevice(1)

    if ai and ai_record:
        # Printing recording device
        ai.record_setup()

        # input data all
        input_data = []
        # turn
        output_data_x = []
        # gas / brake
        output_data_y = []

    elif ai and not ai_record:
        model_x, model_y = ai.model_setup()

    print("F to start")
    F = 0
    while F == 0:
        # if 'F' in key_check():
        F = 1
        print("Running")
        print("Q to break")
        while True:
            check_key = key_check()

            # Start
            video, video_copy = main.start()

            # Finding lines
            lines = main.finding_lines(video, video_copy)

            # Calculations
            main.line_calculations(lines)

            # Keys
            main.driving_mode()

            wait_key, last_time = main.setups(last_time)

            if cv2.waitKey(wait_key) & 0xFF == ord('q'):
                break
            if 'Q' in check_key:
                F = 0
                print("F to continue")
                break
        cv2.destroyAllWindows()
        vjoy.reset()
