F1 2017 game script / Ai drive

Project still work in progress

Project intent to make self-driving script / ai for F1 2018 game using Python

Game.py

Taking ss from game window and finding the best line.

Recording Controller / Wheel positions.

Recording Gas / Brake.

Recording best line position (x-pos, y-pos and slope), added recording speed.

Saving inputs (best line position) and outputs (wheel position and gas), input_data.npy, output_x.npy and output_y.npy.

Added script to drive without Ai training (self.ai = 0).

Training_model.py

Loading recorded data from game.py

Balancing recorded data to same length and shuffling data

Changing output values from [3] to [7]

Training model with balanced data, inputs / outputs