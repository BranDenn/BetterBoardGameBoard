class Game():
    def __init__(self, leds = None, display = None, image = None, draw = None, font = None) -> None:
        self.can_play = True
        self.leds = leds
        self.disp = display
        self.img = image
        self.draw = draw
        self.font = font
        self.ROWS = 11
        self.COLUMNS = 11
        self.OFF = [0, 0, 0]
        self.RED = [255, 0, 0]
        self.BLUE = [0, 0, 255]
        self.WHITE = [255, 255, 255]
        #self.center = [self.disp.width // 2, self.disp.height // 2]
    
    def __del__(self) -> None:
        print(self.__class__.__name__, "has been destructed!")

    def game_display(self, stats : dict) -> None:
        self.draw.rectangle((0, 0, self.disp.width, self.disp.height), fill = (0, 0, 0))
        self.draw.rectangle((0, 0, self.disp.width, 30), fill = (255, 0, 0))
        self.draw.rectangle((0, self.disp.height - 30, self.disp.width, self.disp.height), fill = (255, 0, 0))
        self.draw.text((5, 7.5), self.__class__.__name__, font = self.font, fill = (255, 255, 255))

        for i in range(len(stats)):
            self.draw.text((10, 50 + (20 * i)), 
                           (list(stats.keys())[i], ":", list(stats.values())[i]), 
                           font = self.font, fill = (255, 255, 255))
        
        self.draw.text((5, 135), ("Hold Button for 2s"), font = self.font, fill = (255, 255, 255))
        self.draw.text((5, 145), ("to return to menu."), font = self.font, fill = (255, 255, 255))
        self.disp.display(self.img)

    def update_display(self, stats : dict) -> None:
        self.draw.rectangle((0, 50, self.disp.width, self.disp.height - 50), fill = (0, 0, 0))

        for i in range(len(stats)):
            self.draw.text((10, 50 + (20 * i)), 
                           (list(stats.keys())[i], ":", list(stats.values())[i]), 
                           font = self.font, fill = (255, 255, 255))
            
        self.disp.display(self.img)
        