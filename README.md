# Atari player ai <img src="https://cloud.githubusercontent.com/assets/890250/14069263/4a602094-f4b5-11e5-8a0e-63a236134841.gif" alt="Agent3" height="100" align="right"/>
Based on the deepmind paper on deep Q reinforcement learning. Learns an optimum action policy from pixel level data.

## Python interface instructions
Python interface instructions are available here
[https://github.com/bbitmaster/ale_python_interface/wiki/Code-Tutorial](https://github.com/bbitmaster/ale_python_interface/wiki/Code-Tutorial)

## Score Policy
The score policy is +1/-30 to weed out the random agents. +1 points for surviving in each frame and -30 for colliding with the red brick.


## Screenshots

### A simple agent which does nothing but just sits around
<img src="https://cloud.githubusercontent.com/assets/890250/14069266/4a6c3ce4-f4b5-11e5-8d87-803b27795cee.gif" alt="Agent0" height="100" align="right"/>
This agent just sits around doing nothing. It doesn't take any action, left or right. Looks like someone needs a little motivation in life.

### Random agent
<img src="https://cloud.githubusercontent.com/assets/890250/14069265/4a6bc84a-f4b5-11e5-8f3d-f00cadc44013.gif" alt="Agent1" height="100" align="right"/>
An agent which oscillates between left and right albeit randomly.
The agent oscillates a lot right now.

### 25% accuracy
<img src="https://cloud.githubusercontent.com/assets/890250/14069264/4a63e86e-f4b5-11e5-9732-e26c0ada86d5.gif" alt="Agent2" height="100" align="right"/>
An agent which has learnt to dodge the red brick some times. It gets a score of 2529/10000 = 25% accuracy. The agent still oscillates a lot but lesser than first case. It does run into the red brick occasionaly though.

### 86% accuracy
<img src="https://cloud.githubusercontent.com/assets/890250/14069263/4a602094-f4b5-11e5-8a0e-63a236134841.gif" alt="Agent3" height="100" align="right"/>
An agent which has learnt to dodge the red brick effectively. It get a score of 8698/10000 = 86% accuracy. The agent has learnt that oscillating to and fro heavily is not a really helpful policy and hence is a lot calmer.

It also never runs into the red brick anymore, dodging it like a master samurai.
