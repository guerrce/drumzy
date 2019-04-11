import sys
from LeapPython import Leap

import pygame

from leap_parser import SampleListener
from load_sound import load_sound
from visualize import init_screen
import drum

SCREEN_SIZE = (500, 500)

DRUM_COUNT = 1
DRUM_LIST = []
DRUM_LOCATIONS = []

def main():
    # Note: this works only for two drums
    # Need to be adjusted once we can get user selected drum count
    pygame.mixer.init()
    sound1 = load_sound("sound_clips/Kick1.wav")
    sound2 = load_sound("sound_clips/Snare1.wav")

    drum1Rect = pygame.Rect(0,0,250, 500)
    drum2Rect = pygame.Rect(250,0,250, 500)
    
    example_drum1 = drum.Drum(((-100, -50) , (0, 50)), sound1, drum1Rect)
    example_drum2 = drum.Drum(((0, -50) , (100, 50)), sound2, drum2Rect)

    DRUM_LIST.append(example_drum1)
    DRUM_LIST.append(example_drum2)

    #Initialize visuals
    surface = init_screen(SCREEN_SIZE)

    # Create the listener and controller
    listener = SampleListener(DRUM_LIST,surface)
    controller = Leap.Controller()

    # Have the listener receive events from the controller
    controller.add_listener(listener)

    running = True
    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
                break

        pygame.display.flip()

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)

if __name__ == "__main__":
    main()