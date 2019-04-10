import sys
from LeapPython import Leap
import pygame
from load_sound import load_sound



class SampleListener(Leap.Listener):
    
    def __init__(self, drums):
        Leap.Listener.__init__(self)
        self.drums = drums
        self.sound = load_sound("sound_clips/Kick1.wav")
        self.triggered = False
    

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        print("Exited")

    def on_frame(self, controller):
        # Get the most recent frame and report some basic information
        frame = controller.frame()
        hands = frame.hands
        numHands = len(hands)
        
        for i in range(numHands):
            hand = hands[i]
            palm = hand.palm_position
            print("Palm " + str(i+1) +  " position:", palm)
            
            for drum in self.drums:
                if palm[1] < 150:
                    if drum.in_area(palm):
                        drum.play()
                    drum.trigger()
                else:
                    drum.untrigger()

def main():
    return

if __name__ == "__main__":
    main()