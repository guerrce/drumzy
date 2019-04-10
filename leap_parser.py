import sys
from LeapPython import Leap
import pygame
from load_sound import load_sound



class SampleListener(Leap.Listener):
    """
    def __init__(self, drums):
        self.drums = drums
    """

    def on_init(self, controller):

        pygame.mixer.init()
        self.sound = load_sound("sound_clips/Kick1.wav")
        self.triggered = False
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

        """
        if numHands >= 1:
            hand = hands[0]
            palm = hand.palm_position
            print("Palm 1 position:", palm)

        if numHands >= 2:
            hand = hands[1]
            palm = hand.palm_position
            print("Palm 2 position:", palm)
        """
        
        for i in range(numHands):
            hand = hands[i]
            palm = hand.palm_position
            print("Palm " + str(i+1) +  " position:", palm, "triggered: " + str(self.triggered))
            if palm[1] < 150:
                if not self.triggered:
                    self.sound.play()
                    self.triggered = True
            else:
                self.triggered = False
        


def main():
    # Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    # Have the sample listener receive events from the controller
    controller.add_listener(listener)

    # Keep this process running until Enter is pressed
    print("Press Enter to quit...")
    sys.stdin.readline()

    # Remove the sample listener when done
    controller.remove_listener(listener)

if __name__ == "__main__":
    main()