import sys
from LeapPython import Leap
import pygame
from load_sound import load_sound


ACTIVATION_HEIGHT = 200
class SampleListener(Leap.Listener):
    
    def __init__(self, drums, surface, screen_size):
        Leap.Listener.__init__(self)
        self.drums = drums
        self.surface = surface
        self.triggered = False
        self.screen_size = screen_size
    

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
            border_color = (0,0,0)
            
            for drum in self.drums:
                fill_color = (175, 175, 175)
                if palm[1] < ACTIVATION_HEIGHT:
                    if drum.in_area(palm):
                        drum.play()
                        fill_color = (255, 0, 0)
                    drum.trigger()
                else:
                    drum.untrigger()
                pygame.draw.rect(self.surface, fill_color, drum.rect)
                pygame.draw.rect(self.surface, border_color, drum.rect, 5)

            x = int(((palm[0] + 117.5) / 235) * self.screen_size[0])
            y = int(((palm[2] + 73.5) / 147) * self.screen_size[1])
            cursor_loc = (x,y)

            print("cursor location: ",cursor_loc)
            pygame.draw.circle(self.surface, (0,0,0), cursor_loc, 20)

def main():
    return

if __name__ == "__main__":
    main()