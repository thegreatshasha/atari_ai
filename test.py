from ale_python_interface import ALEInterface
import numpy as np
import pygame

# Create the ale interface and load rom files
ale = ALEInterface()

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

# Initialize a neural network according to nature paper

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
        import pdb; pdb.set_trace()

    print("Episode " + str(episode) + " ended with score: " + str(total_reward))
    ale.reset_game()
