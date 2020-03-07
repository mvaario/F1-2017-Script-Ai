# Calculating average x/y positions
# Calculating slope
# made by mvaario

import numpy as np
import cv2

# Calculating average positions
class calculations:
    # Calculating avg line, saving avg X/Y positions
    def average_line(video, lines, x, y):
        # Changing x/y positions
        x += 425
        y += 185

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

        return x, y

    # Calculating slope
    def slope(x, y, slope):
        # SLOPE
        x = abs(x)
        y = abs(y)

        # Calculating slope
        if y != 0 and x != 0:
            slope = y / x

            # Max slope is 10
            if slope > 10:
                slope = 10

        return slope


