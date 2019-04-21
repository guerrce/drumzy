import sys
from math import ceil
from LeapPython import Leap

import pygame

from leap_parser import SampleListener
from load_sound import load_sound
from visualize import init_screen
import drum

SCREEN_SIZE = (1000, 500)
AREA_SIZE = (235, 147)
MENU_SIZE = 100

DRUM_COUNT = int(sys.argv[1])
DRUM_LIST = []

def main():
    # Note: this works only for two drums
    # Need to be adjusted once we can get user selected drum count
    pygame.mixer.init()
    sound1 = load_sound("sound_clips/Kick1.wav")
    sound2 = load_sound("sound_clips/Snare1.wav")

    drum_rect_width = SCREEN_SIZE[0] - MENU_SIZE

    drum_rect_size = (int(drum_rect_width / DRUM_COUNT) , SCREEN_SIZE[1])
    drum_area_size = (int(AREA_SIZE[0] / DRUM_COUNT), AREA_SIZE[1])

    if DRUM_COUNT > 2:
        drum_rect_size = (int(drum_rect_width / ceil(DRUM_COUNT/2)) , int(SCREEN_SIZE[1]/2))
        drum_area_size = (int(AREA_SIZE[0] / ceil(DRUM_COUNT/2)) , int(AREA_SIZE[1]/2))

    
    rect_x = 0
    rect_y = 0
    area_x = -117
    area_y = -73
    for i in range(DRUM_COUNT):
        sound = sound1
        if i % 2 == 0:
            sound = sound2

        rect = pygame.Rect((rect_x, rect_y), drum_rect_size)
        area = ((area_x, area_y) , (area_x + drum_area_size[0], area_y + drum_area_size[1]))
        d = drum.Drum(area, sound, rect)
        DRUM_LIST.append(d)
        # Make rectangle for visuals
        if DRUM_COUNT <= 2 or i%2 == 1:
            rect_x += drum_rect_size[0]
            rect_y = 0
            area_x += drum_area_size[0]
            area_y = 0
        else:
            rect_y = drum_rect_size[1]
            area_y = 0


        # Calc rectangular area for LEAP control
    

            

    drum1Rect = pygame.Rect(1,1,248, 498)
    drum2Rect = pygame.Rect(251,1,248, 498)
    
    example_drum1 = drum.Drum(((-100, -50) , (0, 50)), sound1, drum1Rect)
    example_drum2 = drum.Drum(((1, -50) , (100, 50)), sound2, drum2Rect)

    #DRUM_LIST.append(example_drum1)
    #DRUM_LIST.append(example_drum2)
    #Initialize visuals
    surface = init_screen(SCREEN_SIZE)

    # Create the listener and controller
    listener = SampleListener(DRUM_LIST,surface, SCREEN_SIZE)
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