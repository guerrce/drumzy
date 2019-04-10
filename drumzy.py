import sys
from LeapPython import Leap

from leap_parser import SampleListener
import drum

DRUM_COUNT = 1

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