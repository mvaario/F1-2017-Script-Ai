# Game F1 2017, intent to make self-driving script / ai
# Taking ss from game window and finding the best line
# Recording Controller / Wheel positions
# Recording Gas / Brake
# Recording best line position (x-pos, y-pos, slope and speed)
# Saving inputs (best line position) and outputs (wheel position and gas), input_data.npy, output_x.npy and output_y.npy
# Added script to drive without Ai training (settings.py ai = False and ai_record = False)
# made by mvaario

from screen import *
from drive import *
from data_balance import *
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

        # speed
        self.v = 1

        # side lines
        self.side = 0


        # old line
        self.line = [5, 5, 5, 5, 5]


        return

    # Screen analysing
    def analyse(self):
        video, video_copy = screen.record()

        finding_lane.turn_start(self, video, video_copy)
        finding_lane.brake_start(self, video, video_copy)
        finding_lane.speed_start(self, video, video_copy)
        finding_lane.side_track(self, video, video_copy)

        return video, video_copy

    # Data balance
    def data(self):
        print("Data balance")

        # input = loading input data ([x, slope, brake, old_brake, v])
        input = np.load('input_data.npy', allow_pickle=True)
        # output_x = loading recorded inputs (turn)
        output_x = np.load('output_x.npy', allow_pickle=True)
        # output_x = loading recorded inputs (gas, brake)
        output_y = np.load('output_y.npy', allow_pickle=True)

        # X-axis balance (len, shape)
        input_x, output_x, input_x_test, output_x_test = balance.x_axis(input, output_x)

        # Y-axis balance (len, shape)
        input_y, output_y, input_y_test, output_y_test = balance.y_axis(input, output_y)

        # Building X-axis model
        model_x = training.model_x(input)

        # Building Y-axis model
        model_y = training.model_y(input)

        # Training models
        training.model_fitting(model_x, model_y,
                               input_x, input_y,
                               output_x, output_y
                               )

        print("")
        print("Full data length:", len(input))
        print("Turning data:", len(input_x))
        print("Straight data:", len(input_y))


        # Testing models
        training.model_testing(model_x, model_y,
                               input_x_test, output_x_test,
                               input_y_test, output_y_test
                               )



        return

    # Drive controls
    def control(self):
        #   SCRIPT KEYS
        if ai is True:
            if record is True:
                ai_record.model_record(self, input_data, output_data_x, output_data_y)
            else:
                ai_drive.model_drive(self, model_x, model_y)
        else:
            script.start(self)
        return


if __name__ == '__main__':
    print("")
    main = main()
    check_key = key_check()
    vjoy.reset()

    if data_balance is True:
        main.data()
    else:
        if ai is True:
            if record is True:
                input_data, output_data_x, output_data_y = options.ai_record()
            else:
                model_x, model_y = options.ai_models()
        else:
            print("Script drive")
        print("")
        print("F to start")
        while True:
            if not running:
                if 'F' in key_check():
                    running = True
                    print("Running")
                    print("Q to break")
            while running:
                check_key = key_check()

                # Start
                video, video_copy = main.analyse()

                # Drive
                main.control()

                # Setup
                options.setups(video)

                if cv2.waitKey(wait_key) & 0xFF == ord('q'):
                    running = False
                    break
                if 'Q' in check_key:
                    running = False
                    print("F to continue")
                    break
            cv2.destroyAllWindows()
            vjoy.reset()
