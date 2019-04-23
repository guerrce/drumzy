import sys
from math import ceil
from LeapPython import Leap

import pygame

from leap_parser import SampleListener
from visualize import init_screen
import drum
import speech_recognition as sr

SCREEN_SIZE = (1000, 500)
AREA_SIZE = (235, 147)
MENU_SIZE = 100

DRUM_COUNT = int(sys.argv[1])
DRUM_LIST = []

def get_sounds():
    kick1 = "sound_clips/Kick1.wav"
    snare1 = "sound_clips/Snare1.wav"
    clap1 = "sound_clips/Clap1.wav"
    cowbell1 = "sound_clips/Cowbell1.wav"
    crash1 = "sound_clips/Crash1.wav"
    #hhc1 = "sound_clips/HighHatC1.wav"
    hho1 = "sound_clips/HighHatO1.wav"
    th1 = "sound_clips/TomHigh1.wav"
    tl1 = "sound_clips/TomLow1.wav"
    #tm1 = "sound_clips/TomMid1.wav"

    return [kick1, snare1, clap1, cowbell1, crash1, hho1, th1, tl1]

def create_drums(count):
    #sound and 
    soundfiles = get_sounds()
    notes  = []
    for i in range(8):
        notes.append(i+1)
    count_to_grid = {1: (1,1), 2: (1,2), 4: (2,2), 6: (2,3), 8: (2,4)}

    if count not in count_to_grid.keys():
        raise ValueError("Cannot have " + count + " drums in grid. Try 1, 2, 4, or 8 drums.")

    #initialize spaces of areas in window
    window_width = SCREEN_SIZE[0] - MENU_SIZE
    window_height = SCREEN_SIZE[1]
    leap_width = AREA_SIZE[0] - MENU_SIZE*AREA_SIZE[0]/SCREEN_SIZE[0]
    leap_depth = AREA_SIZE[1]

    #determine spacing
    (gridrows, gridcols) = count_to_grid[count]
    rect_col_spacing = int(window_width/gridcols)
    rect_row_spacing = int(window_height/gridrows)
    area_col_spacing = int(leap_width/gridcols)
    area_row_spacing = int(leap_depth/gridrows)


    #create drums
    area_offset = [x/2 for x in AREA_SIZE]
    for i in range(count):
        gridpos = (i%gridcols,int(i/gridcols)) #(col number, row number) of row to correspond with pygame x,y coords

        #Create pygame rectangle
        topleft = (rect_col_spacing*gridpos[0],rect_row_spacing*gridpos[1])
        size = (rect_col_spacing, rect_row_spacing)
        rect = pygame.Rect(topleft, size)
        
        topleft = (area_col_spacing*gridpos[0] - area_offset[0] , area_row_spacing*gridpos[1] - area_offset[1])
        botright = (area_col_spacing*(gridpos[0]+1) - area_offset[0] ,area_row_spacing*(gridpos[1]+1) - area_offset[1])
        area = (topleft, botright)
        d = drum.Drum(area, soundfiles[i], rect, notes[i])
        DRUM_LIST.append(d)


def main():
    # Note: this works only for two drums
    # Need to be adjusted once we can get user selected drum count
    pygame.mixer.init()    
    #Initialize visuals
    surface = init_screen(SCREEN_SIZE)

    create_drums(DRUM_COUNT)   

    # Create the listener and controller
    recording = False
    listener = SampleListener(DRUM_LIST,surface, SCREEN_SIZE)
    controller = Leap.Controller()

    # Have the listener receive events from the controller
    controller.add_listener(listener)

    #Speech Recognizer
    r = sr.Recognizer()
    r.pause_threshold = 0.6
    m = sr.Microphone(sample_rate = 16000)

    def callback(recognizer, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            text = recognizer.recognize_google(audio).lower()
            print(text)
            if "start" in text or "spark" in text:
                listener.start_recording(controller)
            elif "stop" in text or "stock" in text:
                listener.stop_recording(controller)
            elif "save" in text or "safe" in text :
                listener.write_wav(controller)
            elif "play" in text:
                listener.play_wav(controller)
            elif "loop in text":
                listener.loop(controller)
        except sr.UnknownValueError:
            pass
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    with m as source:
        r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
                break

            else:
                pass
        pygame.display.flip()

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)

    #stop speech when done
    stop_listening(wait_for_stop=False)

if __name__ == "__main__":
    main()
