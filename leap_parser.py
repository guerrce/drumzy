import sys
from LeapPython import Leap
import pygame
from load_sound import load_sound



class SampleListener(Leap.Listener):
    
    def __init__(self, drums, surface):
        Leap.Listener.__init__(self)
        self.drums = drums
        self.surface = surface
        self.triggered = False
    

    def on_init(self, controller):
        print("Initialized")

    def on_connect(self, controller):
        print("Connected")

    def on_disconnect(self, controller):
        print("Disconnected")

    def on_exit(self, controller):
        pygame.quit()
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
                color = (255, 255, 255)
                if palm[1] < 150:
                    if drum.in_area(palm):
                        drum.play()
                        color = (255, 0, 0)
                    drum.trigger()
                else:
                    drum.untrigger()
                pygame.draw.rect(self.surface, color, drum.rect)

def main():
    return

if __name__ == "__main__":
    main()