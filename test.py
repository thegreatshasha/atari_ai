from ale_python_interface import ALEInterface
import numpy as np
import pygame
from helpers import get_processed_screen
import keras
from keras.models import Sequential
from keras.layers.core import Dense, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.optimizers import SGD
from ring_buffer import RingBuffer

# Create the ale interface and load rom files
ale = ALEInterface()

# Some common settings
HISTORY_LENGTH = 4

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
images = RingBuffer(shape=(1000, 84, 84))
actions = RingBuffer(shape=(1000, 1))
rewards = RingBuffer(shape=(1000, 1))
terminals = RingBuffer(shape=(1000, 1))

# Initialize a neural network according to nature paper
# Defining the neural net architecture
model = Sequential()
model.add(Convolution2D(16, 8, 8, subsample=(4,4), input_shape=(HISTORY_LENGTH,84,84)))
model.add(Activation('relu'))
model.add(Convolution2D(32, 4, 4, subsample=(2,2)))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(256))
model.add(Activation('relu'))
model.add(Dense(legal_actions.shape[0]))
sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='mean_squared_error', optimizer=sgd)
## will SGD work with multiple function calls?


# Version1, let it grow, let it grow
for episode in range(10):
    total_reward = 0.0
    
    # Replace this with fixed time (we can't have loopy episodes)
    while not ale.game_over():

        # get best possible action from the current neural network
        image = get_processed_screen(ale)
        history = np.array([image]*4)
        history_batch = np.array([history])
        prediction = model.predict(history_batch)[0]
        best_action = legal_actions[np.argmax(prediction)]
        
        # act on the best possible action
        reward = ale.act(best_action);
        terminal = 1 if ale.game_over() else 0
        total_reward += reward

        # Store everything in the transition table
        images.push(image)
        actions.push(best_action)
        rewards.push(reward)
        terminals.push(terminal)

        print (images.bottom, images.top)
        if terminal:
            import pdb; pdb.set_trace()

        # check if game over
        #if total_reward != 0:
        #import pdb; pdb.set_trace()


    print("Episode " + str(episode) + " ended with score: " + str(total_reward))
    ale.reset_game()
