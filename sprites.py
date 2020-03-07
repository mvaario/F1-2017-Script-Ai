# Finding best line position
# Finding brake line position
# Drawing lines
# AI setups
# made by mvaario


import cv2
import numpy as np
import pygame
from settings import *
from tensorflow import keras

#Finding best line
class bestline:
    #   TURN
    # Finding best line position
    def region_of_interest_turn(video, video_copy,x):

        # Calculating x_down position
        if x > 200:
            x_down = 100
        elif x < -200:
            x_down = -100
        else:
            x_down = int(x / 2)

        # Calculating y position
        y = abs(int(x/1.5))
        if y > 50:
            y = 50

        # Making area to analyze
        polygons = np.array([[(300+x_down, 170), (550+x_down, 170), (450+x, y), (400+x, y)]])
        # alavasen, alaoikea, yläoikea, keskiylääoikei,  keskiylävasen ,ylävasen

        # Masking video copy, aka making black screen
        mask = np.zeros_like(video_copy)
        # Filling black screen with region
        cv2.fillPoly(mask, polygons, (255, 255, 255))
        # Fitting video on region
        region = cv2.bitwise_and(video_copy, mask)
        # Displaying area on the video
        cv2.fillPoly(video, polygons, (255, 0, 0))

        return region

    # Finding green pixels from the region
    def green_pixels(region):
        # Converting colors (RBG to HSV)
        hsv = cv2.cvtColor(region, cv2.COLOR_RGB2HSV)
        # Define low_green pixels
        low_green = np.array([50, 50, 140])  # 50, 50, 180
        # Define top_green pixels
        up_green = np.array([80, 150, 200])  # 80, 100, 230
        # Displaying all founded the green pixels
        green_pixels = cv2.inRange(hsv, low_green, up_green)
        return green_pixels

# Finding brake line
class brakeline:
    # BRAKE
    # Finding best line position
    def region_of_interest_brake(video, video_copy, x, y, v):
        # Changing avg y-axis
        y += 200
        y2 = int(y / 3) - (10 * v)

        if y < 10:
            y = 10
        if y > 50:
            y = 50
        x = int(x / 2)

        # Making area to analyze
        polygons = np.array([[(410 + x, y), (440 + x, y), (450 + x, y2), (400 + x, y2)]])
        # alavasen, alaoikea, yläoikea, keskiylääoikei,  keskiylävasen ,ylävasen

        # Masking video copy, aka making black screen
        mask = np.zeros_like(video_copy)
        # Filling black screen with region
        cv2.fillPoly(mask, polygons, (255, 255, 255))
        # Fitting video on region
        region = cv2.bitwise_and(video_copy, mask)
        # Displaying area on the video
        cv2.fillPoly(video, polygons, (0, 0, 255))

        return region

    # Finding red pixels from the region
    def red_pixels(region):
        # Converting colors (RBG to HSV)
        hsv = cv2.cvtColor(region, cv2.COLOR_RGB2HSV)
        # Define low_red pixels
        low_red = np.array([110, 50, 120])  # 0, 150, 120       / 110 , 50  , 120
        # Define top_red pixels
        up_red = np.array([160, 255, 245])  # 80, 240, 250     / 160 , 255  , 245
        # Finding red pixels from region
        red_pixels = cv2.inRange(hsv, low_red, up_red)

        return red_pixels

# Finding speedometor
class speedometer:
    #   SPEED
    # Finding speed meter position
    def region_of_interest_speed(video, video_copy):

        # Making area to analyze
        polygons = np.array([[(750, 325), (780, 325), (780, 305), (750, 305)]])
        # alavasen, alaoikea, yläoikea, keskiylääoikei,  keskiylävasen ,ylävasen

        # Masking video copy, aka making black screen
        mask = np.zeros_like(video_copy)
        # Filling black screen with region
        cv2.fillPoly(mask, polygons, (255, 255, 255))
        # Fitting video on region
        region = cv2.bitwise_and(video_copy, mask)
        # Displaying area on the video
        cv2.fillPoly(video, polygons, (100, 100, 100))
        return region

    # Finding white pixels from the region
    def white_pixels(region):
        v = 1

        # Define white color
        white = (255, 255, 255)

        # Getting white pixels region
        pixels = np.argwhere(region == white)
        if pixels.size != 0:

            # Getting max position (x-axis)
            pixels = np.amax(pixels)

            # If speed is more than 100km/h, max pixels will be more than 770
            # Then speed is 2
            if pixels > 770:
                v = 2

        return v

# Drawing lines
class drawing:

    # Displaying bestline
    def bestline(video, green_pixels):

        # Blur and canny  image
        blur = cv2.GaussianBlur(green_pixels, (5, 5), 0)
        canny = cv2.Canny(blur, 0, 0)
        # Finding lines using green pixels
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 1, maxLineGap=35, minLineLength=5)

        # Drawing lines
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(video, (x1, y1), (x2, y2), (0, 0, 255), 1)

        return video, lines

    # Displaying brakeline
    def brakeline(video, red_pixels, x, v, slope, old_brake):
        i = 0

        # Blur and canny image
        blur = cv2.GaussianBlur(red_pixels, (5, 5), 0)
        canny = cv2.Canny(blur, 0, 0)
        # Finding lines
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 1, maxLineGap=10, minLineLength=1)

        # Only drawing lines if speed is 2 and driving straight
        if lines is not None and v == 2 and slope > 8 and abs(x) < 50:
            for line in lines:
                i = i + 1
                x1, y1, x2, y2 = line[0]
                cv2.line(video, (x1, y1), (x2, y2), (255, 255, 255), 1)
            # Braking = line count
            braking = i
        else:
            braking = 0
            # decreasing old braking
            old_brake = old_brake - 5

        # Changing old braking to equal to new brake
        if braking != 0:
            old_brake = braking

        # Making sure brakings cant't be negative
        if braking < 0:
            braking = 0
        if old_brake < 0:
            old_brake = 0

        return braking, old_brake

#  AI setups
class ai:

    # Printing recording info
    def record_setup():

            if save:
                print("AI data recording in on")
            else:
                print("AI recording test is on, not saving")

            # Joystick info
            pygame.display.init()
            pygame.joystick.init()
            pygame.joystick.Joystick(0).init()

            # Printing recording device
            Name = pygame.joystick.Joystick(0).get_name()
            print("Name of the recording device:")
            print(Name)

            return

    # Downloading models
    def model_setup():

        # Loading models
        model_x = keras.models.load_model("x_axis.h5")
        model_y = keras.models.load_model("y_axis.h5")
        print("Loading models")

        return model_x, model_y

    # Changing input data
    def input_shape(x, slope, v, brake, old_brake):

        # Inputs
        input = []
        input.append([x, slope, brake, old_brake, v])

        x = []
        for i in range(len(input)):
            x.append([input[i], [0, 0, 0, 0, 0]])

        input = np.asarray(x)

        return input

