
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

    def __init__(self, area, sound, rect):
        self.area = area
        self.sound = sound
        self.triggered = False
        self.rect = rect

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
        if not self.triggered:
            self.sound.play()
        self.trigger()

    def untrigger(self):
        self.triggered = False