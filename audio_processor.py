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

class NoteList():
    def __init__(self):
        self.notes = []
        self.midi_file = MIDIFile(1)
        self.midi_file.addTempo(TRACK, TIME, BPM)

    def add_note(self, note):
        self.notes.append(note)

    def update_midi(self):
        for note in self.notes:
            self.midi_file.addNote(TRACK, CHANNEL, note.pitch, TIME + note.start_time, DURATION, VOLUME)

    def write_midi(self):
        self.update_midi()
        with open(MIDI_FILENAME, "wb") as output_file:
            self.midi_file.writeFile(output_file)

    def print_list(self):
        for note in self.notes:
            note.print_note()

def main():
    # for testing purposes only

    notes = NoteList()
    t0 = time()
    recording = False
    counter = 0

    key_map = {"a" : 60, 
               "b" : 61, 
               "c" : 62, 
               "d" : 63, 
               "e" : 64}

    while True:
        key = input()
        t = time() - t0
        t = t / (BPM/60)
        print(t)

        if key == "s":    # start
            if not recording:
                print("starting recording round %s" % counter)
                t0 = time()
                recording = True
            else:
                print("already recording!")
        elif key == "t":   # stop
            if recording:
                print("stopped recording")
                recording = False
                notes.update_midi()
            else:
                print("not recording")
        elif key == "q":  # quit
            break
        else:
            if key in key_map.keys():
                notes.add_note(Note(key_map[key], t))
            else:
                notes.add_note(Note(65, t))

    notes.print_list()
    notes.write_midi()
    



if __name__ == '__main__':
    main()