import os
import pygame

def load_sound(name):
    """
    load a sound file and return it 
    param name: string filename of sound file to load
    """
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    try:
        sound = pygame.mixer.Sound(name)
    except pygame.error:
        print ('Cannot load sound:')
        raise SystemExit
    return sound