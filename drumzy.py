import sys
from LeapPython import Leap

import pygame

from leap_parser import SampleListener
from load_sound import load_sound
import drum

SCREEN_SIZE = (1000, 1000)

DRUM_COUNT = 1
DRUM_LIST = []
DRUM_LOCATIONS = []

def main():
	pygame.mixer.init()
	sound1 = load_sound("sound_clips/Kick1.wav")
	sound2 = load_sound("sound_clips/Snare1.wav")
	# Note: this works best for constant drums
	# Need to be adjusted once we can get user selected drum count
	example_drum1 = drum.Drum(((-100, -50) , (0, 50)), sound1)
	example_drum2 = drum.Drum(((0, -50) , (100, 50)), sound2)

	DRUM_LIST.append(example_drum1)
	DRUM_LIST.append(example_drum2)

	# Create a sample listener and controller
	listener = SampleListener(DRUM_LIST)
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