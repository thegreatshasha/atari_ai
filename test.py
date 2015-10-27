from ale_python_interface import ALEInterface
import numpy as np

# Create the ale interface and load rom files
ale = ALEInterface()
ale.loadROM('/Users/shashwat/Downloads/space_invaders.bin')

import pdb; pdb.set_trace()

# These are the set of valid actions in the game
legal_actions = ale.getMinimalActionSet()

# Run actions over each episode randomly and print reward
for episode in range(10):
    total_reward = 0.0
    while not ale.game_over():
        a = legal_actions[np.random.randint(legal_actions.size)]
        reward = ale.act(a);
        total_reward += reward
    print("Episode " + str(episode) + " ended with score: " + str(total_reward))
    ale.reset_game()
