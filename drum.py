from load_sound import load_sound

class Drum():
    """
    class representing a virtual drum

    param area: a tuple of two tuples, where the first tuple is the x and y
                coordinates of drum's top left corner, and the second tuple 
                is the coordinates of the bottom right corner
                These are the coordinates in virtual space using the LEAP convention
    param sound: sound clip attatched to this drum
    param rect: pygame Rectangle for visualization (add this later)
    """

    def __init__(self, area, soundfile, rect, note):
        self.area = area
        self.soundfile = soundfile
        self.sound = load_sound(soundfile)
        self.triggered = False
        self.rect = rect
        self.note = note

    def in_area(self, palm_position):
        x = palm_position[0]
        y = palm_position[2]

        if (self.area[0][0] <= x and x < self.area[1][0] and
            self.area[0][1] <= y and y < self.area[1][1]):
            return True

    def trigger(self):
        if not self.triggered:
            self.triggered = True

    def play(self):
        played = False
        if not self.triggered:
            self.sound.play()
            played = True
        self.trigger()
        return played

    def untrigger(self):
        self.triggered = False

    def note_val(self):
        return self.note