from ale_python_interface import ALEInterface
import numpy as np
import pygame
from helpers import resize_image
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D

# Create the ale interface and load rom files
ale = ALEInterface()

# Some common settings
RESIZE_METHOD = 'crop'
RESIZED_WIDTH = 84
RESIZED_HEIGHT = 84
CROP_OFFSET = 8

# Comment this to disable gui
ale.setBool('display_screen', True)
pygame.init()

# Load the rom
ale.loadROM('/Users/shashwat/Downloads/space_invaders.bin')

# These are the set of valid actions in the game
legal_actions = ale.getMinimalActionSet()

# Run actions over each episode randomly and print reward

# How to get screen rgb?
width, height = ale.getScreenDims()
screen_buffer = np.empty((height, width), dtype=np.uint8)

# Define history variables here
images = []

# Initialize a neural network according to nature paper
# Defining the neural net architecture
model = Sequential()
model.add(Convolution2D(16, 8, 8, subsample=(4,4), input_shape=(4,84,84)))
model.add(Activation('relu'))
model.add(Convolution2D(32, 4, 4, subsample=(2,2)))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dense(legal_actions.shape[0]))
import pdb; pdb.set_trace()

# Version1, let it grow, let it grow
for episode in range(10):
    total_reward = 0.0
    
    # Replace this with fixed time (we can't have loopy episodes)
    while not ale.game_over():

        # Select action from neural net output instead of random weights

        a = legal_actions[np.random.randint(legal_actions.size)]
        reward = ale.act(a);
        total_reward += reward

        # Get buffer data and store it in screen_buffer
        ale.getScreenGrayscale(screen_buffer)

        awesome_image = resize_image(screen_buffer, width, height, RESIZED_WIDTH, RESIZED_HEIGHT, CROP_OFFSET, resize_method = 'crop')
        images.append(awesome_image)
        import pdb; pdb.set_trace()

    print("Episode " + str(episode) + " ended with score: " + str(total_reward))
    ale.reset_game()
