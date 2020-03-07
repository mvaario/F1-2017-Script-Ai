F1 2017 game script / Ai drive

------------------------------

Project still work in progress

------------------------------

Project intent to make self-driving script / ai for F1 2017 game using Python

------------------------------

Game.py

Taking screenshot from game window and finding the best line.

Recording Controller / Wheel positions.

Recording Gas / Brake.

Recording best line position (x-pos, y-pos and slope), added recording speed.

Saving inputs (best line position) and outputs (wheel position and gas), input_data.npy, output_x.npy and output_y.npy.

Script to drive without Ai training (self.ai = 0).

Loading and driving with traned models from training_model.py

------------------------------

training_model.py

Loading recorded data from game.py

Balancing recorded data to same length and shuffling data

Changing input and output data dimensions

Changing output lens from [3] to [7]

Training model with balanced data, inputs / outputs

------------------------------

Demonstration video on youtube

https://www.youtube.com/watch?v=ErdoywyTK10&feature=youtu.be
