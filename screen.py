# Everything for screen analysing
# - Finding best line
# - Finding braking line
# - Checking speed
# - Calculating average lines
# - Drawing lines
# made by mvaario

from settings import *
import cv2
from grabscreen import grab_screen
import numpy as np

class screen:

    # Recording game window
    def record():
        # If user is using dual monitor setup
        if dual_monitor:
            # Checking ai from settings
            if ai and record:
                video = grab_screen(region=(-pos_x_max, pos_y_min, -pos_x_min, pos_y_max))
            else:
                video = grab_screen(region=(-pos_x_max, pos_y_min, -pos_x_min, pos_y_max))
            # Converting colors BGR to RGB
            video = cv2.cvtColor(video, cv2.COLOR_BGR2RGB)

        else:
            print("No video")
            quit()

        # Resizing the window
        video = cv2.resize(video, (size_x, size_y))
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

    # Best line area
    def turn_region(self, video, video_copy):
        x = self.x
        side = self.side
        # Calculating x_down position

        x_d = int((x / 1.5) + side)
        x = int(x + side)
        y = int(size_y * 0.08)

        # Making area to analyze
        polygons = np.array([[(int(size_x * 0.31400) + x_d, y * 7),
                              (int(size_x * 0.68600) + x_d, y * 7),
                              (int(size_x * 0.54675) + x, y),
                              (int(size_x * 0.45325) + x, y)
                              ]])
        # alavasen
        # alaoikea
        # yläoikea
        # ylävasen

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

    # Braking area
    def brake_region(self, video, video_copy):
        # Changing avg y-axis
        x = self.x / 1.2
        slope = self.slope / 2
        v = (self.v - 1) * 10
        side = self.side

        x = int((x) + side)
        y = int(abs(x/2) - v - slope + 20)

        if y > int(size_y * 0.16327):
            y = int(size_y * 0.16327)

        # Making area to analyze
        polygons = np.array([[(int(size_x * 0.46168) + x, int(size_y * 0.16327)),
                              (int(size_x * 0.53832) + x, int(size_y * 0.16327)),
                              (int(size_x * 0.52524) + x, y),
                              (int(size_x * 0.47477) + x, y)
                              ]])
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
        # Checking if speed is over 100 km/h
        region = finding_lane.speed_region(self, video, video_copy)
        calculations.white_pixels(self, region)

        return

    # Speedo meter region
    def speed_region(self, video, video_copy):
        # Making area to analyze
        polygons = np.array([[(int(size_x * 0.94), size_y),
                              (size_x, size_y),
                              (size_x, int(size_y * 0.92)),
                              (int(size_x * 0.94), int(size_y * 0.92))
                              ]])
        # alavasen, alaoikea, yläoikea, keskiylääoikei,  keskiylävasen ,ylävasen

        mask = np.zeros_like(video_copy)
        cv2.fillPoly(mask, polygons, (255, 255, 255))
        region = cv2.bitwise_and(video_copy, mask)
        cv2.fillPoly(video, polygons, (100, 100, 100))

        return region

    # Side track
    def side_track(self, video, video_copy):
        region = finding_lane.side_track_region(self, video, video_copy)
        green_pixels = finding_lane.green_pixels(region)
        calculations.side_line(self, green_pixels)
        return

    # Side track region
    def side_track_region(self, video, video_copy):
        x = self.x
        side = self.side

        # Calculating x_down position
        x_d = int((x / 1.5) + side)
        x = int(x + side)

        y = int(size_y * 0.08)

        # Making area to analyze
        polygons_left = np.array([[(int(size_x * 0.25794) + x_d, y * 7),
                                   (int(size_x * 0.31401) + x_d, y * 7),
                                   (int(size_x * 0.41496) + x, y),
                                   (int(size_x * 0.32336) + x, y * 2)
                                   ]])

        polygons_right = np.array([[(int(size_x * 0.68598) + x_d, y * 7),
                                    (int(size_x * 0.74206) + x_d, y * 7),
                                    (int(size_x * 0.67664) + x, y * 2),
                                    (int(size_x * 0.585045) + x, y)
                                    ]])

        # alavasen, alaoikea, yläoikea, ylävasen

        # Masking video copy, aka making black screen
        mask = np.zeros_like(video_copy)

        # Filling black screen with region
        cv2.fillPoly(mask, polygons_left, (255, 255, 255))
        cv2.fillPoly(mask, polygons_right, (255, 255, 255))
        # Fitting video on region
        region = cv2.bitwise_and(video_copy, mask)
        # Displaying area on the video
        cv2.fillPoly(video, polygons_left, (255, 255, 0))
        cv2.fillPoly(video, polygons_right, (255, 255, 0))

        return region


# Drawing lines
class drawing:

    # Drawing turning lines
    def bestline(video, green_pixels):
        # Blur and canny image
        blur = cv2.GaussianBlur(green_pixels, (5, 5), 0)
        canny = cv2.Canny(blur, 0, 0)
        # Finding lines using green pixels
        lines = cv2.HoughLinesP(canny, 1, np.pi / 180, 1, maxLineGap=35, minLineLength=5)
        point = []
        # Drawing lines
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(y1 - y2) > 2:
                    cv2.line(video, (x1, y1), (x2, y2), (0, 0, 255), 1)
                    point.append(line)
                    lines = np.asarray(point)

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

        point = []

        # Only drawing lines if speed is 2 and driving straight
        if lines is not None and v == 2 and slope > 1 and x < 25:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                if abs(y1 - y2) > 1:
                    i = i + 1
                    cv2.line(video, (x1, y1), (x2, y2), (255, 255, 255), 1)
                    point.append(line)
                    lines = np.asarray(point)

            # Braking = line count
            braking = i
        else:
            braking = 0
            # decreasing old braking
            old_brake = old_brake - 5

        # Changing old braking to equal to new brake
        if braking != 0:
            if braking > 10:
                braking = 10
            old_brake = braking

        # Making sure braking cant't be negative
        if braking < 0:
            braking = 0
        if old_brake < 0:
            old_brake = 0

        self.brake = braking
        self.old_brake = old_brake

        return


# Calculating average positions
class calculations:
    # Calculating avg line, saving avg X/Y positions
    def average_line(self, video, lines):
        x = self.x + size_x/2
        y = self.y + size_y/2

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
            if x > size_x/2:
                x -= 1
            elif x < size_x/2:
                x += 1
            y = 0

        # Drawing average line
        cv2.line(video, (int(x) - 10, int(size_y*0.75)),
                        (int(x) + 10, int(size_y*0.75)),
                        (0, 255, 0), 5)

        # Changing points back to normal form
        x -= size_x/2
        y -= size_y/2
        # Making sure points stay in the right area
        if x > size_x*0.37383:
            x = size_x*0.37383
        if x < -size_x*0.37383:
            x = -size_x*0.37383

        self.x = x
        self.y = y


        return

    # Calculating speed
    def white_pixels(self, region):
        # Define white color
        white = (255, 255, 255)

        # Getting white pixels region
        pixels = np.argwhere(region == white)
        if pixels.size != 0:
            # Getting max position (x-axis)
            pixels = np.amax(pixels)

            # If speed is more than 100km/h
            if pixels > int(size_x*0.99):
                v = 2
            else:
                v = 1

            self.v = v
        return

    # Calculating slope
    def slope(self):
        # SLOPE
        x = abs(self.x)
        y = abs(self.y)


        # Calculating slope
        if y != 0 and x != 0:
            slope = y / x * 2
            # print(x)
            # print(slope)
        else:
            slope = self.slope - 1
            if slope < 0:
                slope = 0

        # Max slope is 10
        if slope > 20:
            slope = 20

        self.slope = slope
        return

    # Calculating side position
    def side_line(self, green_pixels):
        pixel_left = 0
        pixel_right = 0

        white = 255
        # Getting white pixels
        pixels = np.argwhere(green_pixels == white)
        if pixels.size != 0:
            pixels = pixels[0]
            pixels = pixels[1]
            # print(pixels)

            if pixels < int(size_x*0.45608) and self.x <= 0:
                pixel_left = np.amax(pixels)
                pixel_left = pixel_left
            if pixels > int(size_x*0.54393) and self.x >= 0:
                pixel_right = np.amin(pixels)
                pixel_right = abs(pixel_right - size_x)
            if pixel_right != 0 or pixel_left != 0:
                self.side = (pixel_left - pixel_right) / 12
        else:
            if self.side < -0.5:
                self.side += 0.5
            elif self.side > 0.5:
                self.side -= 0.5
            else:
                self.side = 0

        return
