# Atari player ai <img src="https://cloud.githubusercontent.com/assets/890250/14069263/4a602094-f4b5-11e5-8a0e-63a236134841.gif" alt="Agent3" height="100" align="right"/>
Based on the deepmind paper on deep Q reinforcement learning. Learns an optimum action policy from pixel level data.

## Python interface instructions
Python interface instructions are available here
[https://github.com/bbitmaster/ale_python_interface/wiki/Code-Tutorial](https://github.com/bbitmaster/ale_python_interface/wiki/Code-Tutorial)

## The game
We tested the agent on a really simple game, dodge the brick. The aim of the game is for the green brick to dodge the onslaught of the falling red bricks
The score policy is +1/-30 to weed out the random agents. +1 points for surviving in each frame and -30 for colliding with the red brick and dying.

## Screenshots

### A simple agent which does nothing but just sits around
<img src="https://cloud.githubusercontent.com/assets/890250/14069266/4a6c3ce4-f4b5-11e5-8d87-803b27795cee.gif" alt="Agent0" height="100" align="right"/>
This agent just sits around doing nothing. It doesn't take any action, left or right. Looks like someone needs a little motivation in life.

### Random agent
<img src="https://cloud.githubusercontent.com/assets/890250/14069265/4a6bc84a-f4b5-11e5-8f3d-f00cadc44013.gif" alt="Agent1" height="100" align="right"/>
An agent which oscillates a lot, staying at the same place rougly. It also runs into the red brick a lot and isn't really being affected by the red brick's presence.

### 25% accuracy
<img src="https://cloud.githubusercontent.com/assets/890250/14069264/4a63e86e-f4b5-11e5-9732-e26c0ada86d5.gif" alt="Agent2" height="100" align="right"/>
An agent which tries to move away from the red brick and find a safe spot. It gets a score of 2529/10000 = 25% accuracy. The agent still oscillates a lot but lesser than first case. It does run into the red brick occasionally though.

### 86% accuracy
<img src="https://cloud.githubusercontent.com/assets/890250/14069263/4a602094-f4b5-11e5-8a0e-63a236134841.gif" alt="Agent3" height="100" align="right"/>
An agent which has learnt to dodge the red brick effectively. It get a score of 8698/10000 = 86% accuracy. The agent has learnt that oscillating to and fro heavily is not a really helpful policy and hence is a lot calmer.

It also never runs into the red brick anymore, dodging it like a master samurai.

## Running on the rest of atari games
Coming soon
