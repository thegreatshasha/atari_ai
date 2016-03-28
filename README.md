# Atari player ai
Based on the deepmind paper on deep Q reinforcement learning. Learns an optimum action policy from pixel level data.

## Python interface instructions
Python interface instructions are available here
[https://github.com/bbitmaster/ale_python_interface/wiki/Code-Tutorial](https://github.com/bbitmaster/ale_python_interface/wiki/Code-Tutorial)

## Score Policy
The score policy is +1/-30 to weed out the random agents. +1 points for surviving in each frame and -30 for colliding with the red brick.


## Screenshots
A simple agent which does nothing but just sits around

<img src="https://cloud.githubusercontent.com/assets/890250/14069263/4a602094-f4b5-11e5-8a0e-63a236134841.gif" alt="Drawing" style="height: 100px;"/>

An agent which oscillates between left and right albeit randomly

An agent which has learnt to dodge the red brick some times. It gets a score of 2529/10000 = 25% accuracy. The agent still oscillates a lot but lesser than first case.

An agent which has learnt to dodge the red brick effectively. It get a score of 8698/10000 = 86% accuracy. The agent has learnt that oscillating to and fro heavily is not a really helpful policy and dodges bricks at the last moment like a master samurai!
