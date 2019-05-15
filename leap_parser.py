import sys
from LeapPython import Leap
import pygame
from load_sound import load_sound
import threading
from visualize import init_screen
from textbox import multiLineSurface

from wav_processor import Note, NoteList
from time import time, sleep


ACTIVATION_HEIGHT = 200
UNTRIGGERED_DRUM_COLOR = (0, 175, 175) # gray
TRIGGERED_DRUM_COLOR = (255, 0, 0)       # red
BORDER_COLOR = (0,0,0)                   # black
BORDER_SIZE = 5
MIDI_FILE = "test_midi.mid"
WAV_FILE = "output.wav"
METRONOME_BPM = 100

pygame.font.init()
#print(pygame.font.get_fonts())
myfont = pygame.font.SysFont("cambria", 35)
otherfont = pygame.font.SysFont("arial", 18)

class SampleListener(Leap.Listener):
    
    def __init__(self, drums, surface, screen_size):
        Leap.Listener.__init__(self)
        self.drums = drums
        self.surface = surface
        self.triggered = False
        self.screen_size = screen_size
        self.recording = False
        self.looping = False
        self.notes = NoteList()
        self.t0 = time()
        self.countin = load_sound("sound_clips/CountIn1.wav")
        self.metronome_started = True
        self.metronome_t0 = time()
        self.metronome_rect = pygame.Rect(903, 30, 94, 460)


        ins_string = ("Commands: \n"
                     "Start: Begin recording of initial sound" + "\n"
                     "Stop: Stop recording of sound, either after start or stop" + "\n"
                     "Save: Save output to WAV file" + "\n"
                     "Play: Play the current WAV file" + "\n"
                     "     -(Save before using this command)" + "\n"
                     "Loop: Play the current recording in a loop, and record over that")
        print(ins_string)
        box = pygame.Rect((self.screen_size[0]-290, 5), (280, 400))
        multiLineSurface(ins_string, otherfont, box, (255,255,255), self.surface, (self.screen_size[0] - 290, 5))

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

    def stop_recording(self, controller, stop_loop = True):
        print("Recording Stopped")
        self.recording = False
        if stop_loop:
            self.looping = False
            print("looping stopped")
        self.notes.update_wav()

    def start_metronome(self, controller):
        self.metronome_t0 = time()
        self.metronome_started = True


    def stop_metronome(self,controller):
        self.metronome_started = False

    def write_wav(self, controller):
        print("Saving...")
        self.notes.write_wav(WAV_FILE)
        print("Done Saving")

    def play_wav(self, controller):
        measure = load_sound(WAV_FILE)
        measure.play()

        return measure.get_length()

    def loop(self, controller):
        self.looping = True
        
        def loop_thread():
            wait_time = 0
            local_start = time()
            while self.looping:
                if not self.recording:
                    self.start_recording(controller)
                    wait_time = self.play_wav(controller)
                if time() - local_start > wait_time:
                    local_start = time()
                    self.stop_recording(controller, stop_loop=False)
                    self.write_wav(controller)
        threading.Thread(target = loop_thread).start()

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information

        frame = controller.frame()
        hands = frame.hands
        numHands = len(hands)

        #metronome stuff
        if self.metronome_started:
            t = time()
            if t % (60.0/METRONOME_BPM) < 0.1:
                pygame.draw.rect(self.surface, TRIGGERED_DRUM_COLOR, self.metronome_rect)
            else:
                pygame.draw.rect(self.surface, (0,0,0), self.metronome_rect)
        
        # Drum and hand stuff
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

                name = drum.soundfile[12:-5]
                image = drum.image
                pic_rect = image.get_rect()
                pic_rect.center = drum.rect.center
                self.surface.blit(image, pic_rect)



            x = int(((palm[0] + 117.5) / 235) * self.screen_size[0])
            y = int(((palm[2] + 73.5) / 147) * self.screen_size[1])
            cursor_loc = (x,y)

            #print("cursor location: ",cursor_loc)
            pygame.draw.circle(self.surface, (0,0,0), cursor_loc, 20)
def main():
    return

if __name__ == "__main__":
    main()