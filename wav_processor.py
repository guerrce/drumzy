import sys
import math
from time import time
from pydub import AudioSegment

BPM = 60
VOLUME = 100
DURATION = 1
TRACK = 0
CHANNEL = 0
TIME = 0

class Note():
    def __init__(self, wavfile, start_time):
        self.wavfile = wavfile
        self.start_time = start_time #seconds

    def print_note(self):
        return (self.wavfile,self.start_time)

class NoteList():
    def __init__(self):
        self.notes = []
        self.sound = AudioSegment.empty()

    def add_note(self, note):
        self.notes.append(note)

    def update_wav(self):
        newsound = AudioSegment.empty()
        for note in self.notes:
            nextsound = AudioSegment.from_wav(note.wavfile)
            nextend = len(nextsound) + 1000*note.start_time #Audiosegment is in milliseconds
            overallend = len(newsound)
            silence = AudioSegment.silent(duration = max(nextend, overallend))
            witholdsound = silence.overlay(newsound)
            newsound = witholdsound.overlay(nextsound, position = note.start_time*1000)
        self.sound = newsound

    def write_wav(self, filename = "output.wav"):
        self.update_wav()
        self.sound.export(filename, format = 'wav')   

    def print_list(self):
        for note in self.notes:
            note.print_note()

def main():
    # for testing purposes only

    notes = NoteList()
    t0 = time()
    recording = False
    counter = 0

    key_map = {"a" : "sound_clips/Kick1.wav", 
               "b" : "sound_clips/Snare1.wav", 
               "c" : "sound_clips/Clap1.wav", 
               "d" : "sound_clips/Cowbell1.wav"}

    while True:
        key = input()
        t = time() - t0
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
                notes.update_wav()
            else:
                print("not recording")
        elif key == "q":  # quit
            break
        else:
            if key in key_map.keys():
                notes.add_note(Note(key_map[key], t))

    notes.print_list()
    notes.write_wav()
    



if __name__ == '__main__':
    main()