# Game F1 2017, intent to make self-driving script / ai
# Taking ss from game window and finding the best line
# Recording Controller / Wheel positions
# Recording Gas / Brake
# Recording bestline position (x-pos, y-pos, slope and speed)
# Saving inputs (best line position) and outputs (wheel position and gas), input_data.npy, output_x.npy and output_y.npy
# Added script to drive without Ai training (settings.py ai = False and ai_record = False)
# made by mvaario


from settings import *
import cv2
import numpy as np
from grabscreen import grab_screen


class screen:

    # Recording game window
    def record():
        # If user is using dual monitor setup
        if dual_monitor:
            # Checking ai from settings
            if ai and record:
                # video = grab_screen(region=(-width, height, width + 1180, height + 349))
                video = grab_screen(region=(-1920, 0, 0, 1080))
            else:
                # video = grab_screen(region=(-1700, 400, -850, 770))
                video = grab_screen(region=(-1920, 0, 0, 1080))
            # Converting colors BGR to RGB
            video = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)

        else:
            print("No video")
            running = False
            return running

        # Resizing the window
        video = cv2.resize(video, (851, 349))
        # Making copy of the window
        video_copy = np.copy(video)

        return video, video_copy


# Finding bestline
class finding_lane:

    # TURN
    def turn_start(self, video, video_copy):

        region = finding_lane.turn_region(self, video, video_copy)

        green_pixels = finding_lane.green_pixels(region)
        video, lines = drawing.bestline(video, green_pixels)

        calculations.average_line(self, video, lines)
        calculations.slope(self)

        return

    # Best line region
    def turn_region(self, video, video_copy):
        x = self.x

        # Calculating x_down position
        if x > 200:
            x_down = 100
        elif x < -200:
            x_down = -100
        else:
            x_down = int(x / 2)

        # Calculating y position
        y = abs(int(x / 1.5))
        if y > 50:
            y = 50

        # Making area to analyze
        polygons = np.array([[(300 + x_down, 170), (550 + x_down, 170), (450 + x, y), (400 + x, y)]])
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



    # BRAKE
    def brake_start(self, video, video_copy):
        region = finding_lane.brake_region(self, video, video_copy)

        red_pixels = finding_lane.red_pixels(region)

        drawing.brakeline(self, video, red_pixels)

        return
    # Finding best line position

    def brake_region(self, video, video_copy):
        # Changing avg y-axis
        x = self.x
        y = self.y + 200
        v = self.v
        v = 10
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



    # SPEED
    def speed_start(self, video, video_copy):
        region = finding_lane.speed_region(self,video, video_copy)
        calculations.white_pixels(self, region)

        return

    # Speedo meter region
    def speed_region(self, video, video_copy):

        if ai is not True or record is not True:
            polygons = np.array([[(750, 350), (780, 350), (780, 320), (750, 320)]])
        else:
            polygons = np.array([[(780, 350), (810, 350), (810, 320), (780, 320)]])
        # alavasen, alaoikea, yläoikea, keskiylääoikei,  keskiylävasen ,ylävasen

        mask = np.zeros_like(video_copy)
        cv2.fillPoly(mask, polygons, (255, 255, 255))
        region = cv2.bitwise_and(video_copy, mask)
        cv2.fillPoly(video, polygons, (100, 100, 100))

        return region



# Drawing lines
class drawing:

    # Drawing turning lines
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

    # Drawing braking lines
    def brakeline(self, video, red_pixels):
        v = self.v
        slope = self.slope
        x = self.x
        old_brake = self.old_brake
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


        self.braking = braking
        self.old_braking = old_brake

        return




# Calculating average positions
class calculations:
    # Calculating avg line, saving avg X/Y positions
    def average_line(self, video, lines):
        x = self.x + 425
        y = self.y + 185
        # Changing x/y positions
        # x += 425
        # y += 185

        x1_avg = 0
        x2_avg = 0
        y1_avg = 0
        y2_avg = 0
        i = 0

        # Adding lines start and end points together
        if lines is not None:
            for line in lines:

                x1 = np.array(line)[0, 0]
                x2 = np.array(line)[0, 2]
                y1 = np.array(line)[0, 1]
                y2 = np.array(line)[0, 3]

                # Adding x points
                x1_avg = np.add(x1_avg, x1)
                x2_avg = np.add(x2_avg, x2)

                # Adding y points
                y1_avg = np.add(y1_avg, y1)
                y2_avg = np.add(y2_avg, y2)
                i = i + 1

            # Calculating starting and ending points averages
            x1 = x1_avg / i
            x2 = x2_avg / i

            y1 = y1_avg / i
            y2 = y2_avg / i

            # Calculating x and y average
            x = (x1 + x2) / 2
            y = (y1 + y2) / 2

        # Changing old positing if lines were not found
        else:
            if x > 470:
                x -= 1
            elif x < 380:
                x += 1

        # Drawing average line
        x = int(x)
        y = int(y)
        cv2.line(video, (x - 10, 150), (x + 10, 150), (0, 255, 0), 5)

        # Changing points back to normal form
        x -= 425
        y -= 185
        # Making sure points stay in the right area
        if x > 200:
            x = 200
        if x < -200:
            x = -200

        self.x = x
        self.y = y

        return

    # Calculating speed
    def white_pixels(self, region):
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
        self.v = v

        return

    # Calculating slope
    def slope(self):
        # SLOPE
        x = abs(self.x)
        y = abs(self.y)

        # Calculating slope
        if y != 0 and x != 0:
            slope = y / x
        else:
            slope = self.slope

            # Max slope is 10
            if slope > 10:
                slope = 10

        self.slope = slope
        return