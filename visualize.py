"""
stuff for visualization
"""

import pygame

def init_screen(size):
	"""
	Initialize pygame visuals
	param width: int tuple width and height of window respecively
	return: pygame screen object created
	"""
	pygame.init()
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption('Drumzy')
	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	screen.blit(background, (0, 0))
	return screen
