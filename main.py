# Game F1 2017, intent to make self-driving script / ai
# Taking ss from game window and finding the best line
# Recording Controller / Wheel positions
# Recording Gas / Brake
# Recording best line position (x-pos, y-pos, slope and speed)
# Saving inputs (best line position) and outputs (wheel position and gas), input_data.npy, output_x.npy and output_y.npy
# Added script to drive without Ai training (settings.py ai = False and ai_record = False)
# made by mvaario

from data_balance import *
from drive import *
from screen import *
import time
from getkeys import key_check
import cv2

class main:
    def __init__(self):

        # x/y-axis average
        self.x = 0
        self.y = 0
        self.slope = 0


        # Braking
        self.brake = 0
        self.old_brake = 0

        # Aggression
        self.ag = 20

        # speed
        self.v = 1

        return

    # Start / Recording game window
    def analyse(self):
        video, video_copy = screen.record()

        finding_lane.turn_start(self, video, video_copy)
        finding_lane.brake_start(self, video, video_copy)
        finding_lane.speed_start(self, video, video_copy)

        return video, video_copy

    # Data balance
    def data(self):

        # input = loading input data ([x, slope, brake, old_brake, v])
        input = np.load('input_data.npy', allow_pickle=True)
        # output_x = loading recorded inputs (turn)
        output_x = np.load('output_x.npy', allow_pickle=True)
        # output_x = loading recorded inputs (gas, brake)
        output_y = np.load('output_y.npy', allow_pickle=True)

        input_x = input
        input_y = input

        # X-axis balance (len, shape)
        input_x, output_x = balance.x_axis(input_x, output_x)

        # Y-axis balance (len, shape)
        input_y, output_y = balance.y_axis(input_y, output_y)

        # model X-axis
        training.model_x(input_x, output_x)

        # model Y-axis
        training.model_y(input_y, output_y)

        print("Full data lenght", len(input))
        print("Turning data", len(input_x))
        print("Straight data", len(input_y))

        return

    # Drive controls
    def control(self):
        #   SCRIPT KEYS
        if ai is True:
            if record is True:
                ai_record.model_record(self, input_data, output_data_x, output_data_y)
            else:
                ai_drive.model_drive(self, model_x, model_y)
            pass
        else:
            script.start(self)

        return



if __name__ == '__main__':
    print("")
    main = main()
    last_time = time.time()
    check_key = key_check()

    if data_balance is True:
        main.data()
    else:
        if ai is True:
            if record is True:
                input_data, output_data_x, output_data_y = options.ai_record()
                print("")
            else:
                model_x, model_y = options.ai_models()
                print("")
        else:
            print("Script drive")
            print("")

        print("F to start")
        while not running:
            # if 'F' in key_check():
                print("Running")
                print("Q to break")
                while True:
                    check_key = key_check()

                    # Start
                    video, video_copy = main.analyse()

                    main.control()

                    # Setup
                    last_time = options.setups(last_time, video)


                    if cv2.waitKey(wait_key) & 0xFF == ord('q'):
                        break
                    if 'Q' in check_key:
                        F = 0
                        print("F to continue")
                        break
                cv2.destroyAllWindows()
                vjoy.reset()
