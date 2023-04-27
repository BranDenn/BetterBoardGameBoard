class Game():
    def __init__(self, leds = None, display = None) -> None:
        self.can_play = True
        self.leds = leds
        self.display = display
        self.ROWS = 11
        self.COLUMNS = 11
        self.OFF = [0, 0, 0]
    
    def __del__(self):
        print(self.__class__.__name__, "has been destructed!")
