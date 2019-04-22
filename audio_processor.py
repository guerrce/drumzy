import sys
import math
from time import time
from midiutil import MIDIFile

BPM = 60
VOLUME = 100
DURATION = 1
TRACK = 0
CHANNEL = 0
TIME = 0
MIDI_FILENAME = "test_midi.mid"

class Note():
    def __init__(self, pitch, start_time):
        self.pitch = pitch
        self.start_time = start_time

    def print_note(self):
        print("Pitch: %s, Start: %s" % (self.pitch, self.start_time))

def main():
    notes = []
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(TRACK, TIME, BPM)

    # for testing purposes only
    print("Press Enter to start recording")
    sys.stdin.readline()
    print("recording")
    t0 = time()
    
    while True:
        key = input()
        t = time() - t0
        tt = t / (BPM/60)
        print(tt)

        if key == "a":
            notes.append(Note(60, tt))
        elif key == "s":
            notes.append(Note(62, tt))
        elif key == "q":
            break
        else:
            notes.append(Note(63, tt))

    for note in notes:
        note.print_note()
        MyMIDI.addNote(TRACK, CHANNEL, note.pitch, TIME + note.start_time, DURATION, VOLUME)

    with open(MIDI_FILENAME, "wb") as output_file:
        MyMIDI.writeFile(output_file)



if __name__ == '__main__':
    main()