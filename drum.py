
class Drum():
    """
    class representing a virtual drum

    param area: a tuple of two tuples, where the first tuple is the x and y
                coordinates of drum's top left corner, and the second tuple 
                is the coordinates of the bottom right corner
    param sound: sound clip attatched to this drum ( still not sure how to do this)
    """

    def __init__(self, area, sound):
        self.area = area
        self.sound = sound
        self.triggered = False