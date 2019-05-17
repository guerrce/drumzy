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

def getoffsetsandcoincidents(basetimelist, newtimelist, tolerance = 0.1):
    offsets = []
    coincidents = 0
    for i in newtimelist:
        closest = min(basetimelist, key = lambda x: abs(x-i))
        diff = closest-i
        offsets.append(diff)
        if abs(diff) < tolerance:
            coincidents += 1
    return (offsets, coincidents)

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
        #might need to modify this class to take in an 'oldrecording' parameter in the future and overlay the old recording with a new recording in update_wav

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

    def combine_with_new(self, newnotelist):
        if len(self.notes) == 0:
            #simple if there are no previous notes
            self.notes = [x for x in newnotelist.notes]
            return

        #Determine how similar the two notelists are by comparing the new times to the OG times
        notetimes = [x.start_time for x in self.notes]
        othernotetimes = [x.start_time for x in newnotelist.notes]

        #Without any modification, what are offsets and the number of same time beats?
        offsets, initnum_coincident = getoffsetsandcoincidents(notetimes, othernotetimes)

        #Try some offsets to see if they make anything better
        bestnumcoincident = 0
        bestoffset = None
        for i in offsets:
            if abs(i) < 1:
                updatenotetimes = [x+i for x in othernotetimes]
                print(updatenotetimes)
                newoffsets, newnum_coincident = getoffsetsandcoincidents(notetimes, updatenotetimes, 0.25)
                if newnum_coincident > bestnumcoincident:
                    bestnumcoincident = newnum_coincident
                    bestoffset = i

        #update with offset if offset causes 25% improvement on coincidents
        newnotes = newnotelist.notes
        print(bestnumcoincident)
        print(initnum_coincident)
        if bestnumcoincident > 1.25 * initnum_coincident:
            createnotelist = NoteList()
            for i in newnotes:
                createnotelist.add_note(Note(i.wavfile, i.start_time + bestoffset))
            newnotes = createnotelist.notes
        self.notes = sorted(self.notes + newnotes, key = lambda x: x.start_time)
        print([x.start_time for x in self.notes])



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