# Game F1 2017, intent to make self-driving script / ai
# Taking ss from game window and finding the best line
# Recording Controller / Wheel positions
# Recording Gas / Brake
# Recording best line position (x-pos, y-pos and slope), added recording speed
# Saving inputs (best line position) and outputs (wheel position and gas), input_data.npy, output_x.npy and output_y.npy
# Added script to drive without Ai training (self.ai = 0)
# made by mvaario

import cv2
import numpy as np
import time
from grabscreen import grab_screen
from getkeys import key_check
import pyvjoy
import pygame
from tensorflow import keras


class settings:
    def __init__(self):

        # ai = 0 -> script, 1 -> tensorflow
        self.ai = 1
        self.ai_record = 0
        self.aggression = 50

        # Setupsf
        self.display = 1
        self.fps = 0


        # speed
        self.speed = 1

        # regions
        self.y = 0
        self.x = 0

        # turn
        self.avg = 0
        self.avg_y = 0
        self.slope = 50

        # braking
        self.braking_force = 0
        self.old_braking_force = 0
        self.old_y = 0

        # Tensorflow
        self.tf_x = 0
        self.tf_y = 0

        # test
        self.input = []

        return

    # Taking screenshot from game window(tested with double screen setup, game resolution 1282x766), (region=(-1700, 400, -850, 770))
    def start():
            if game.ai == 1 and game.ai_record == 1:
                video =  grab_screen(region=(370, 454, 1550, 975))
            else:
                video = grab_screen(region=(-1700, 400, -850, 770))

            video = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)
            return video

    #   SPEED
    # Finding speed meter position
    def region_of_interest_speed(video_copy, video):
        if game.ai != 1 and game.ai_record != 1:
            polygons = np.array([[(750, 350), (780, 350), (780, 320), (750, 320)]])
        else:
            polygons = np.array([[(780, 350), (810, 350), (810, 320), (780, 320)]])
        # alavasen, alaoikea, yläoikea, keskiylääoikei,  keskiylävasen ,ylävasen

        mask = np.zeros_like(video_copy)
        cv2.fillPoly(mask, polygons, (255, 255, 255))
        masked_white = cv2.bitwise_and(video_copy, mask)
        cv2.fillPoly(video, polygons, (100, 100, 100))

        return masked_white
    def white_pixels(video):
        hsv = video
        low_white = np.array([160, 170, 190])  # 50, 50, 180
        up_white = np.array([255, 255, 255])  # 80, 100, 230
        white_pixels = cv2.inRange(hsv, low_white, up_white)
        # cv2.imshow("test", white_pixels)
        return white_pixels
    # Chekking if speed is >100, saving self.speed
    def speed_check(white_pixels, video):

        blur = cv2.GaussianBlur(white_pixels, (5, 5), 0)
        canny = cv2.Canny(blur, 5, 5)
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 1, maxLineGap=10, minLineLength=1)

        speed = 1

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]

                cv2.line(video, (x1, y1), (x2, y2), (0, 0, 0), 2)

                x1 = np.array(line)[0, 0]
                x2 = np.array(line)[0, 2]
                # print(x1)
                if x1 > 770 or x2 > 770:
                    speed = 2

        game.speed = speed

        return video


    #   TURN
    # Finding best line position
    def region_of_interest_turn(video_copy, video):
        x_ylä = int(game.avg)
        y = 0
        if x_ylä > 200:
            x_ala = 100
        elif x_ylä < -200:
            x_ala = -100
        else:
            x_ala = int(x_ylä / 2)

        y = abs(int(x_ylä/1.5))
        if y > 50:
            y = 50

        # polygons = np.array([[(762, 680), (800, 680), (800, 650), (762, 650)]])
        polygons = np.array([[(300+x_ala, 170), (550+x_ala, 170), (450+x_ylä, y), (400+x_ylä, y)]])
        # alavasen, alaoikea, yläoikea, keskiylääoikei,  keskiylävasen ,ylävasen

        mask = np.zeros_like(video_copy)
        cv2.fillPoly(mask, polygons, (255, 255, 255))
        masked_green = cv2.bitwise_and(video_copy, mask)
        cv2.fillPoly(video, polygons, (255, 0, 0))

        game.y = y
        game.x = x_ylä

        return masked_green
    # Checking green pixels from best line
    def green_pixels(video):
        hsv = cv2.cvtColor(video, cv2.COLOR_RGB2HSV)
        low_green = np.array([50, 50, 140])  # 50, 50, 180
        up_green = np.array([80, 150, 200])  # 80, 100, 230
        green_pixels = cv2.inRange(hsv, low_green, up_green)
        # cv2.imshow("test", green_pixels)
        return green_pixels
    # Displaying best line lines
    def turning_line(green_pixels, video):

        blur = cv2.GaussianBlur(green_pixels, (5, 5), 0)
        canny = cv2.Canny(blur, 0, 0)
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 1, maxLineGap=35, minLineLength=5)

        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(video, (x1, y1), (x2, y2), (0, 0, 255), 1)
        return video, lines
    # Calculating avg line, saving avg X/Y positions(self.x1/x2/y1/y2) and slopes
    def average_line(lines):
        old_avg = game.avg + 425
        old_avg_y = game.avg_y + 185

        x1_avg = 0
        x2_avg = 0
        y1_avg = 0
        y2_avg = 0
        i = 0

        if lines is not None:
            for line in lines:
                x1 = np.array(line)[0, 0]
                x2 = np.array(line)[0, 2]
                y1 = np.array(line)[0, 1]
                y2 = np.array(line)[0, 3]

                x1_avg = np.add(x1_avg, x1)
                x2_avg = np.add(x2_avg, x2)

                y1_avg = np.add(y1_avg, y1)
                y2_avg = np.add(y2_avg, y2)
                i = i + 1


            # AVG
            x1_avg = x1_avg / i
            x2_avg = x2_avg / i

            y1_avg = y1_avg / i
            y2_avg = y2_avg / i

            avg = (x1_avg + x2_avg) / 2
            avg_y = (y1_avg + y2_avg) / 2

        else:
            avg = old_avg
            avg_y = old_avg_y
            if avg > 470:
                avg = avg - 1
            elif avg < 380:
                avg = avg + 1

        x = int(avg)
        y = int(avg_y / 1.58)
        cv2.line(video, (x - 10, 200-y), (x + 10, 200-y), (0, 255, 0), 5)

        avg = avg - 425
        avg_y = avg_y - 185
        if avg > 200:
            avg = 200
        if avg < -200:
            avg = -200

        game.avg = avg
        game.avg_y = avg_y

        # SLOPE
        x = abs(game.avg)
        y = abs(game.avg_y)
        slope = game.slope
        if y != 0 and x != 0:
            slope = y / x
            if slope > 50 or slope == 0:
                slope = 50
        game.slope = slope

        return


    #   BRAKE
    # Finding braking line position
    def region_of_interest_brake(video_copy, video):
        v = game.speed
        y = game.y + 30
        y2 = int(y/2) - (10 * v)

        if y < 10:
            y = 10
        if y > 50:
            y = 50
        x = int(game.x / 2)

        polygons = np.array([[(410+x, y), (440+x, y), (450+x, y2), (400+x, y2)]])
        # alavasen, alaoikea, yläoikea, keskiylääoikei,  keskiylävasen ,ylävasen

        mask = np.zeros_like(video_copy)
        cv2.fillPoly(mask, polygons, (255, 255, 255))
        masked_red = cv2.bitwise_and(video_copy, mask)
        cv2.fillPoly(video, polygons, (0, 0, 255))

        # cv2.imshow(winname, masked_red)

        return masked_red
    # Finding red pixels
    def red_pixels(video):

        hsv = cv2.cvtColor(video, cv2.COLOR_RGB2HSV)

        low_red = np.array([110, 50, 120])  # 0, 150, 120       / 110 , 50  , 120
        up_red = np.array([160, 255, 245])  # 80, 240, 250     / 160 , 255  , 245
        red_pixels = cv2.inRange(hsv, low_red, up_red)
        # cv2.imshow("test", reds)
        return red_pixels
    # Displaying braking lines. Saving amount braking lines found, self.braking_force
    def braking_line(red_pixels, video):
        braking = game.braking_force
        old_brake = game.old_braking_force
        i = 0
        blur = cv2.GaussianBlur(red_pixels, (5, 5), 0)
        canny = cv2.Canny(blur, 0, 0)
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 1, maxLineGap=10, minLineLength=1)

        if lines is not None and game.speed == 2 and game.slope > 25 and abs(game.x) < 50:
            for line in lines:
                i = i + 1
                x1, y1, x2, y2 = line[0]
                cv2.line(video, (x1, y1), (x2, y2), (255, 255, 255), 1)
            braking = i
        else:
            braking = 0
            old_brake = old_brake - 5

        if braking != 0:
            old_brake = braking
        if braking < 0:
            braking = 0
        if old_brake < 0:
            old_brake = 0


        game.braking_force = braking
        game.old_braking_force = old_brake

        return video, lines


    #   SCRIPT KEYS
    # Script drive(if self.ai == 0)
    def keys():
        settings.turn()
        settings.speed()
        vjoy.update()
        return
    # Changing virtual controller x-axis
    def turn():

        x = game.avg
        slope = game.slope *2
        speed = game.speed

        ss = slope / 20 + speed
        if ss == 0:
            ss = 1

        x = 16400 + x * 41 / ss

        x = int(x)
        vjoy.data.wAxisX = 0x0 + x

        return
    # Changing virtual controller y-axis
    def speed():

        # GAS
        ag = game.aggression
        v = game.speed
        slope = game.slope
        x = abs(game.avg)

        # prosentit!
        x = (x / 200) * 8200
        slope = (1.1 - slope / 50) * 8200
        ag = (100 - ag) * 25
        v = 7500 - 1 / v * 10000

        y = x + slope + v + ag
        if y > 16400:
            y = 16400

        # BRAKE
        c = settings.brake()
        if c != 0:
            y = c

        y = int(y)
        vjoy.data.wAxisY = 0x0 + y


        return
    # Checking if braking_force != 0, changing virtual controller y-axis
    def brake():
        braking = game.braking_force
        old_braking = game.old_braking_force

        ag = game.aggression
        v = game.speed
        slope = game.slope
        x = abs(game.avg)
        c = 0

        if braking != 0 and old_braking == 0:
            braking = 20
            old_braking = 20
        if braking > 20:
            braking = 20
        if old_braking > 20:
            old_braking = 20

        braking = braking * 2
        old_braking = old_braking * 1.5
        # Prosentit
        braking = 0.025 * braking * 8200
        old_braking = 0.0333 * old_braking * 8200

        c = 16400 + braking + old_braking

        return c


    #   TENSORFLOW
    # Saving inputs and outputs
    def model_record():
        pygame.event.pump()

        x = game.avg
        slope = game.slope
        v = game.speed
        brake = game.braking_force
        old_brake = game.old_braking_force

        # Inputs
        input_data.append([x, slope, brake, old_brake, v])

        # Turn record
        left, straight, right = settings.x_position()
        output_data_x.append([left, straight, right])

        # Gas/Braking record
        gas, zero, brake = settings.y_position()
        output_data_y.append([gas, zero, brake])


        if len(input_data) % 250 == 0:
            print("Frames", len(input_data))
            # np.save("input_data", input_data)
            # print(output_data_x)
            # np.save("output_x", output_data_x)
            # np.save("output_y", output_data_y)

        return
    # Recording x-axis (Turing keys)
    def x_position():

        # Prints the values for axis0-4
        axis = float(pygame.joystick.Joystick(0).get_axis(0))
        # -1 to 1
        left = [0]
        straight = [0]
        right = [0]

        if axis < -0.005:
            if axis < -0.9995:
                axis = -1
            left = [abs(axis)]

        elif axis > 0.005:
            if axis > 0.9995:
                axis = 1
            right = [axis]
        else:
            straight = [1]

        return left, straight, right
    # Recording y-axis (Gas / braking keys)
    def y_position():

        # Prints the values for axis0-4

        gas = [0]
        zero = [0]
        brake = [0]

        # Gas 1 to -1
        gas = float(pygame.joystick.Joystick(0).get_axis(2))
        gas = (gas * -1 + 1) / 2
        if gas > 0.999:
            gas = 1
        if gas < 0.005:
            gas = 0

        # Braking
        brake = float(pygame.joystick.Joystick(0).get_axis(3))
        brake = 1 - brake
        if brake > 0.999:
            brake = 1
        if brake < 0.005:
            brake = 0

        if gas == 0 and brake == 0:
            zero = 1


        return gas, zero, brake



    def model_drive(model_x, model_y):



        # Input shape change
        input = settings.input_change()

        model = model_x
        prediction = model.predict(input)

        k = int(np.argmax(prediction))

        if k == 3:
            k = "straight", k
        elif k > 3:
            k = "Right", k
        else:
            k = "left", k
        print("Moves ", k)
        print("---------")



        return


    def input_change():
        x = game.avg
        slope = game.slope
        v = game.speed
        brake = game.braking_force
        old_brake = game.old_braking_force

        # Inputs
        input = []
        input.append([x, slope, brake, old_brake, v])

        x = []
        for i in range(len(input)):
            x.append([input[i], [0, 0, 0, 0, 0]])

        input = np.asarray(x)

        return input








    #   SETUPS
    # Displaying video and FPS
    def setups(self, last_time):
        winname = "F1 screen"
        # Displaying video
        if game.display == 1:
            cv2.imshow(winname, video)
            if game.ai == 1 and game.ai_record == 1:
                cv2.moveWindow(winname, -880, 40)
            else:
                cv2.moveWindow(winname, 1000, 40)
        # Printing fps, note waitkey
        if game.fps == 1:
            print(round(1/(time.time() - last_time)))
            last_time = time.time()

        return last_time


if __name__ == '__main__':

    game = settings()
    last_time = time.time()
    check_key = key_check()
    vjoy = pyvjoy.VJoyDevice(1)

    # Loading models
    model_x = keras.models.load_model("x_axis.h5")
    model_y = keras.models.load_model("y_axis.h5")

    # Printing recording device
    if game.ai == 1 and game.ai_record == 1:
        # Joystick settings.....
        pygame.display.init()
        pygame.joystick.init()
        pygame.joystick.Joystick(0).init()

        # Prints the joystick's name
        JoyName = pygame.joystick.Joystick(0).get_name()
        print("Name of the joystick:")
        print(JoyName)

        # input data all
        input_data = []
        # turn
        output_data_x = []
        # gas / brake
        output_data_y = []

    print("F to start")
    F = 0
    while F == 0:
        if 'F' in key_check():
            F = 1
            print("Running")
            print("Q to break")
            while True:
                check_key = key_check()

                video = settings.start()
                video = cv2.resize(video, (851, 371))
                video_copy = np.copy(video)


                # print(video.shape)




                # SPEED CHECK > 100!
                masked_white = settings.region_of_interest_speed(video_copy, video)
                white_pixels = settings.white_pixels(masked_white)
                video = settings.speed_check(white_pixels, video)

                # TURNING LINE
                region = settings.region_of_interest_turn(video_copy, video)
                green_pixels = settings.green_pixels(region)
                video, lines = settings.turning_line(green_pixels, video)
                average_line = settings.average_line(lines)

                # BRAKING LINE
                region = settings.region_of_interest_brake(video_copy, video)
                red_pixels = settings.red_pixels(region)
                video, lines = settings.braking_line(red_pixels, video)

                # Script and Tensorflow
                if game.ai == 0:
                    settings.keys()
                elif game.ai == 1:
                    if game.ai_record == 1:
                        settings.model_record()
                    else:
                        settings.model_drive(model_x, model_y)
                else:
                    print("Error")
                    F = 0

                # Setups (FPS print and Display)
                last_time = game.setups(last_time)

                if game.ai_record == 1:
                    wait_key = 100
                else:
                    wait_key = 1
                if cv2.waitKey(wait_key) & 0xFF == ord('q'):
                    break
                if 'Q' in check_key:
                    F = 0
                    print("F to continue")
                    break
            cv2.destroyAllWindows()
            vjoy.reset()
