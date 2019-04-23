import sys
from LeapPython import Leap
import pygame
from load_sound import load_sound
from audio_processor import Note, NoteList
from time import time

ACTIVATION_HEIGHT = 200
UNTRIGGERED_DRUM_COLOR = (175, 175, 175) # gray
TRIGGERED_DRUM_COLOR = (255, 0, 0)       # red
BORDER_COLOR = (0,0,0)                   # black
BORDER_SIZE = 5

class SampleListener(Leap.Listener):
    
    def __init__(self, drums, surface, screen_size):
        Leap.Listener.__init__(self)
        self.drums = drums
        self.surface = surface
        self.triggered = False
        self.screen_size = screen_size
        self.recording = False
        self.notes = NoteList()
        self.t0 = time()
    

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        pygame.quit()
        print("Exited")

    def start_recording(self, controller):
        print("woo")
        self.t0 = time()
        self.recording = True

    def stop_recording(self, controller):
        self.recording = False
        self.notes.update_midi()

    def write_midi(self, controller):
        notes.write_midi()

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        hands = frame.hands
        numHands = len(hands)
        
        for i in range(numHands):
            t = time() - self.t0
            hand = hands[i]
            palm = hand.palm_position
            #print("Palm " + str(i+1) +  " position:", palm)
            
            for drum in self.drums:
                fill_color = UNTRIGGERED_DRUM_COLOR
                if palm[1] < ACTIVATION_HEIGHT:
                    if drum.in_area(palm):
                        drum.play()
                        fill_color = TRIGGERED_DRUM_COLOR
                        if self.recording:
                            self.notes.add_note(Note(drum.note_val(), t))
                    drum.trigger()
                else:
                    drum.untrigger()
                pygame.draw.rect(self.surface, fill_color, drum.rect)
                pygame.draw.rect(self.surface, BORDER_COLOR, drum.rect, BORDER_SIZE)

            x = int(((palm[0] + 117.5) / 235) * self.screen_size[0])
            y = int(((palm[2] + 73.5) / 147) * self.screen_size[1])
            cursor_loc = (x,y)

            #print("cursor location: ",cursor_loc)
            pygame.draw.circle(self.surface, (0,0,0), cursor_loc, 20)

def main():
    return

if __name__ == "__main__":
    main()