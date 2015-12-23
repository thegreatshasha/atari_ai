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
import time
import random
from select_with_probability import select_with_probability
import matplotlib.pyplot as plt
from visualize import Plotter
from games.simple_game import GameManager
import sys

# Create the ale interface and load rom files
#ale = ALEInterface()
ale = GameManager()
ale.add_object({
    'dimensions': (1,3,1,1),
    'type': 'player',
    'color': (0,255,0)
})
ale.add_object({
    'dimensions': (0,1,1,1),
    'type': 'enemy',
    'color': (255,0,0)
})
#ale.setBool('display_screen', True)
#pygame.init()

# csv hack
import csv
fi = open('data.csv', 'w')
wr = csv.writer(fi, delimiter=',')

# Load the rom
ale.loadROM('/Users/shashwat/Downloads/pong.bin')

# These are the set of valid actions in the game
legal_actions = ale.getMinimalActionSet()

# How to get screen rgb?
width, height = ale.getScreenDims()
screen_buffer = np.empty((height, width), dtype=np.uint8)

# Some common settings
HISTORY_LENGTH = 4
MAX_STEPS = 100
MAX_EPOCHS = 20
MINIBATCH_SIZE = 32
LONG_PRESS_TIMES = 1
GAMMA  = 0.9
EPSILON = 0.1
UPDATE_FREQUENCY = 4
MAX_LIVES = ale.lives()
MODE = sys.argv[1]
if MODE == "test":
    MODEL_FILE = sys.argv[2]

episode_sum = 0
episode_sums = []

# Define history variables here
images = RingBuffer(shape=(MAX_STEPS, width, height))
actions = RingBuffer(shape=(MAX_STEPS, 1))
rewards = RingBuffer(shape=(MAX_STEPS, 1))
terminals = RingBuffer(shape=(MAX_STEPS, 1))

# Initialize a neural network according to nature paper
# Defining the neural net architecture
model = Sequential()
model.add(Convolution2D(8 , 4, 4, subsample=(2,2), input_shape=(HISTORY_LENGTH,width,height)))
model.add(Activation('relu'))
model.add(Convolution2D(8, 2, 2, subsample=(1,1)))
model.add(Activation('relu'))
model.add(Flatten())
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(legal_actions.shape[0]))
#rmsp = keras.optimizers.RMSprop(lr=0.001, rho=0.9, epsilon=1e-6)
adadelta = keras.optimizers.Adadelta(lr=1.0, rho=0.95, epsilon=1e-6)
#sgd = SGD(lr=0.0001, decay=1e-6)
model.compile(loss='mean_squared_error', optimizer=adadelta)
if MODE == "test":
    model.load_weights(MODEL_FILE)
## will SGD work with multiple function calls?

# plotter variable
#plotter = Plotter()

def epsilon(step, epoch):
    if epoch == 0:
        return max((MAX_STEPS - float(step))/MAX_STEPS, 0.1)
    else:
        return 0.1

## First define prototype of all the functions here
def get_observation():
     return ale.getScreenGrayScale()
     #return get_processed_screen(ale)

def am_i_dead():
    # If game over / lives decreased.
    if ale.lives() < MAX_LIVES or ale.game_over():
        return True
    return False

# Choose action from max + random strategy
def choose_action(image, step, epoch):
    history = np.array([image]*4)
    history_batch = np.array([history])
    prediction = model.predict(history_batch)[0]
        
    best_action = legal_actions[np.argmax(prediction)]
    random_action = random.choice(legal_actions)
    #EPSILON = 1.0
    if MODE == "test":
        EPSILON = 0.0
    elif MODE == "random":
        EPSILON = 1.0
    else:
        EPSILON = epsilon(step, epoch)
    action = select_with_probability([random_action, best_action], [EPSILON, 1-EPSILON])
    print "Step: %d, Epsilon: %f, Epoch: %d" % (step, EPSILON, epoch)
    return best_action

def long_press(action):
    # Repeat an action and return reward
    global episode_sum
    reward = 0

    for times in range(LONG_PRESS_TIMES):
        reward += ale.act(action)
    
    episode_sum += reward
    print "Episode sum: %d" % episode_sum
    #reward = np.clip(reward, -1, 1)

    return  reward

# Circular buffer's index is always in a wierd position since bottom, top keep moving as more items are added
#  Convert it back to 0, max
def transformed(index, bottom, length):
    return (index - bottom) % length

def get_random_minibatch():
    X_batch = []
    Y_batch = []
    indexes = images.indexes()

    while len(X_batch) < MINIBATCH_SIZE:
        random_index = random.choice(indexes)
        next_index = (random_index+1) % images.length
        # Transformed index
        transformed_index = transformed(random_index, images.bottom, images.length) 

        # If the transformde index is not within the necessary range
        if transformed_index < HISTORY_LENGTH - 1 or transformed_index == transformed(images.top-1, images.bottom, images.length):
            continue

        left = random_index-HISTORY_LENGTH+1

        #if left <= 0:
        #    import pdb; pdb.set_trace()
        
        #print "bottom: %d, top: %d, random: %d" % (images.bottom, images.top, random_index)
        try:
            state1 = images.get(left, random_index+1)#images[left:random_index+1]
            state2 = images.get(left+1, random_index+2)
            #state2 = images[random_index-HISTORY_LENGTH+2:random_index+2]
        except AttributeError:
            import pdb; pdb.set_trace()
            #state1 = images[left:random_index+1]

        # If the first state is terminal, it's the end of an episode and transitioning to an episode doesn't make sense
        if terminals[random_index]:
            continue

        output1 = get_network_output(state1)
        output2 = get_network_output(state2)
        X = state1
        
        Y = np.copy(output1)
        action_index = np.argmax(legal_actions==actions[random_index])
        
        # If the subsquent state is terminal, Q_2_a is zero since it's the teminal step
        #print "Reward %d" % rewards[random_index]
        if terminals[next_index]:
            Y[action_index] = rewards[random_index]
        else:
            Q_2_a = np.max(output2)
            #print "Q2a: %d" % Q_2_a
            Y[action_index] = rewards[random_index] + GAMMA * Q_2_a

        X_batch.append(X)
        Y_batch.append(Y)

    return np.array(X_batch), np.array(Y_batch)
        

def get_network_output(state):
    history_batch = np.array([state])
    prediction = model.predict(history_batch)[0]
    return prediction

# Sample minibatcg of transitions and run gradient gradient_descent
def gradient_descent():
    if images.length >= MINIBATCH_SIZE:
        X_batch, Y_batch =  get_random_minibatch()
        model.fit(X_batch, Y_batch, batch_size=32, nb_epoch=1)

def save_weights(epoch, episode_sums, episode_sum):
    if len(episode_sums) and episode_sum > max(episode_sums):
        filename = "models/model2_%d_%d.hdf5" % (episode_sum, epoch)
        model.save_weights(filename)

def reset(epoch):
    # Append the latest episode sum
    global episode_sum
    global episode_sums
    
    save_weights(epoch, episode_sums, episode_sum)


    episode_sums.append(episode_sum)
    wr.writerow([epoch, episode_sum])
    fi.flush()
    #plotter.write(epoch, episode_sum)
    episode_sum = 0

    ale.reset_game()
    print "Resetting"
    #long_press(0)
    #long_press(0)

# Main loop
for epoch in range(MAX_EPOCHS):
    print "New epoch: %d\n" % epoch
    reset(epoch)

    for step in range(MAX_STEPS):
        # Keep note of the fact that we don't have the concept of an episode unlike nathan's implementation
        image = get_observation()
        
        best_action = choose_action(image, step, epoch)
        
        # get best possible action from the current neural network
        images.push(image)
        actions.push(best_action)

        # If the current state is dead, push 0 reward and mark state as terminal. then reset and continue loop execution
        if am_i_dead():
            terminals.push(1)
            rewards.push(0)
            reset(epoch)
            continue
        
        # Still alive, still alive!
        terminals.push(0)
        
        # long press the best action because humans press keys for longer durations
        reward = long_press(best_action)
        rewards.push(reward)

        if MODE == "test":
            time.sleep(0.1)

        # Train the network on the existing data
        if step % UPDATE_FREQUENCY == 0 and MODE=="train":
            print "umm"
            gradient_descent()