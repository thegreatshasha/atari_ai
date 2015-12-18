import numpy as np
import random
import time
import pygame
import cv2
import cv2.cv as cv

# Helpers here
def transform(dimensions, factor):
	#### VERY INEFFICIENT, CHANGE THIS ASAP
	return tuple([factor*d for d in dimensions])

COLORS = {
	'black': (0,0,0),
	'red': (255, 0, 0),
	'blue': (0,0,255)
}

class GameObject:
	def __init__(self, config):
		pygame.init()
		self.x, self.y, self.width, self.height = config['dimensions']
		self.type = config['type']
		self.color = config['color']

	def get_dimensions(self):
		return (self.x, self.y, self.width, self.height)

class GameManager:
	def __init__(self):
		self.size = (4,4)
		self.scalefactor = 10
		self.transformed_size = transform(self.size, self.scalefactor)

		#self.score = 0

		self.screen = pygame.display.set_mode(self.transformed_size)
		self.enemies = []
		self.player = None
		self.actions = [-1, +1]

		self.record = False
		self.record_zoom = 10
		self.record_frames = []

		self.record_file = 'games/frames'

	""" Proxy methods. These methods provide a proxy for the arcade learning environment"""
	def getMinimalActionSet(self):
		return np.array([0, 1])

	def loadROM(self, romfile):
		print "Why the hell do i need a romfile?"

	def lives(self):
		return 1

	def reset_game(self):
		""" We should try resetting the game and see what happens """
		return 1

	def game_over(self):
		return False

	def getScreenDims(self):
		return self.transformed_size

	def zoomForRecording(self, rgb):
		return np.repeat(np.repeat(rgb,self.record_zoom,axis=0),self.record_zoom,axis=1)
	        
	def recordFrames(self, rgb):
		if self.record_frames:
			self.record_frames.append(self.zoomForRecording(rgb))
			np.save(self.record_file, self.record_frames)
			#self.video.run(self.zoomForRecording(rgb))

	def getScreenRGB(self):
		rgb = pygame.surfarray.pixels3d( self.screen )
		rgb_transformed = np.flipud(np.rot90(rgb, k=1))
		return rgb_transformed

	def getScreenGrayScale(self):
		rgb = self.getScreenRGB()
		#import pdb; pdb.set_trace()
		self.recordFrames(rgb)
		return np.dot(rgb[...,:3], [0.299, 0.587, 0.144])

	def act(self, index):
		self.player.x = np.clip(self.player.x + self.actions[index], 0, self.size[0]-1)
		return self.run()

	def add_object(self, config):
		obj = GameObject(config)

		if obj.type == 'enemy':
			self.enemies.append(obj)
		else:
			self.player = obj

	def handle_events(self):
		events = pygame.event.get()
		for event in events:
		    if event.type == pygame.KEYDOWN:
		        if event.key == pygame.K_LEFT:
		         	self.act(0)
		        if event.key == pygame.K_RIGHT:
		            self.act(1)

	def draw_objects(self):
		for obj in self.enemies:
			pygame.draw.rect(self.screen, obj.color, transform(obj.get_dimensions(), self.scalefactor))

		pygame.draw.rect(self.screen, self.player.color, transform(self.player.get_dimensions(), self.scalefactor))			

	def update(self):
		#import pdb; pdb.set_trace()
		for obj in self.enemies:
			obj.y += 1
			if obj.y > self.size[1]:
				obj.y = 0
				obj.x = random.choice(range(0, self.size[0]))

			if obj.x == self.player.x and obj.y == self.player.y:
				reward = -30
				print "boom"
				return reward

		reward = 1

		return reward

	def run(self):

		self.screen.fill(COLORS['black'])

		reward = self.update()

			# player random action
		#self.handle_events()
			#self.act(random.choice([0,1]))
			
		# draw objects
		self.draw_objects()

		pygame.display.flip()
		return reward

class RandomAgent:

	def __init__(self, ale):
		print "Hi"
		self.ale = ale
		self.score = 0

	def run(self):
		while True:
			time.sleep(0.1)
			self.score += self.ale.act(random.choice([0, 1]))
			print "Score: %d" % self.score



if __name__ == "__main__":
	gm = GameManager()
	gm.add_object({
		'dimensions': (1,3,1,1),
		'type': 'player',
		'color': COLORS['blue']
	})
	gm.add_object({
		'dimensions': (0,1,1,1),
		'type': 'enemy',
		'color': COLORS['red']
	})
	agent = RandomAgent(gm)
	agent.run()