import sys
from LeapPython import Leap

import pygame

from leap_parser import SampleListener
from load_sound import load_sound
import drum

SCREEN_SIZE = (1000, 1000)

DRUM_COUNT = 4
DRUM_LIST = []
DRUM_LOCATIONS = []

def main():
	# Note: this works best for constant drums
	# Need to be adjusted once we can get user selected drum count
	for drum in range(DRUM_COUNT):
		pass

	# Create a sample listener and controller
	listener = SampleListener()
	controller = Leap.Controller()

	# Have the sample listener receive events from the controller
	controller.add_listener(listener)

	"""
	# Initialize GUI
	pygame.init()
	screen = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption('Drumzy')
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((250, 250, 250))

	screen.blit(background, (0, 0))
	pygame.display.flip()

	for event in pygame.event.get():
	    if event.type == QUIT:
	        return
	"""

	# Keep this process running until Enter is pressed
	print("Press Enter to quit...")
	sys.stdin.readline()

	# Remove the sample listener when done
	controller.remove_listener(listener)

if __name__ == "__main__":
    main()