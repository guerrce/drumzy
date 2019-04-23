import sys
from LeapPython import Leap
import pygame
from load_sound import load_sound

from wav_processor import Note, NoteList
from time import time


ACTIVATION_HEIGHT = 200
UNTRIGGERED_DRUM_COLOR = (175, 175, 175) # gray
TRIGGERED_DRUM_COLOR = (255, 0, 0)       # red
BORDER_COLOR = (0,0,0)                   # black
BORDER_SIZE = 5
MIDI_FILE = "test_midi.mid"
WAV_FILE = "output.wav"

pygame.font.init()
#print(pygame.font.get_fonts())
myfont = pygame.font.SysFont("cambria", 35)

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
        self.countin = load_sound("sound_clips/CountIn1.wav")
        #FluidSynth('drumzy_font.sf2')
    

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

        print("Recording Started")
        self.t0 = time()
        self.recording = True

    def stop_recording(self, controller):
        print("Recording Stopped")
        self.recording = False
        self.notes.update_wav()

    def write_wav(self, controller):
        print("Saving...")
        self.notes.write_wav(WAV_FILE)

    def play_wav(self, controller):
        load_sound(WAV_FILE).play()

    def loop(self, controller):
        self.play_wav(controller)
        self.start_recording(controller)

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
                        played = drum.play()
                        fill_color = TRIGGERED_DRUM_COLOR
                        #print(drum.triggered)
                        if self.recording and played:
                            print((drum.soundfile,t))
                            self.notes.add_note(Note(drum.soundfile, t))
                    drum.trigger()
                else:
                    drum.untrigger()

                name = drum.soundfile[12:-5]
                label = myfont.render(name, 1, (0,255,0))

                rect1 = pygame.draw.rect(self.surface, fill_color, drum.rect)
                self.surface.blit(label, rect1)

                rect2 = pygame.draw.rect(self.surface, BORDER_COLOR, drum.rect, 5)
                self.surface.blit(label, rect2)

            x = int(((palm[0] + 117.5) / 235) * self.screen_size[0])
            y = int(((palm[2] + 73.5) / 147) * self.screen_size[1])
            cursor_loc = (x,y)

            #print("cursor location: ",cursor_loc)
            pygame.draw.circle(self.surface, (0,0,0), cursor_loc, 20)

def main():
    return

if __name__ == "__main__":
    main()